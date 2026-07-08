"""
全库元数据只读审计脚本（口径修正版）
扫描 gt_monitor.public 下所有真实 BASE TABLE (relkind='r')，生成注释质量审计报告。

修正点：
- 主表限定 relkind='r'（ordinary table），排除 view/matview/foreign table
- 字段查询通过 IN 子句限定到主表集合
- col_comment_index 只用主表字段做证据池
- 新增 excluded_objects.csv 记录被排除对象

严格只读 —— 不执行任何写操作。
"""
import csv
import os
from collections import defaultdict
from datetime import datetime

import psycopg2

OUTPUT_DIR = r"E:\3\code\metadata_audit"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 数据库连接（与 agent_config.py 一致）──────────────────────────────
CONN = psycopg2.connect(
    host="localhost", port=5433, database="gt_monitor",
    user="postgres", password="test123456",
)
CONN.set_session(readonly=True, autocommit=True)


def query(sql):
    """只读查询辅助"""
    cur = CONN.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    return [dict(zip(cols, r)) for r in rows]


# ══════════════════════════════════════════════════════════════════════
# 1. 构建主表集合（relkind='r' 的 ordinary table）
# ══════════════════════════════════════════════════════════════════════

print("→ 扫描 public schema 真实 BASE TABLE (relkind='r') …")

main_tables_sql = """
SELECT
    t.table_schema,
    t.table_name,
    pgc.relkind,
    pg_catalog.obj_description(pgc.oid, 'pg_class') AS table_comment
FROM information_schema.tables t
JOIN pg_catalog.pg_class pgc ON pgc.relname = t.table_name
JOIN pg_catalog.pg_namespace pgn
  ON pgn.oid = pgc.relnamespace
 AND pgn.nspname = t.table_schema
WHERE t.table_schema = 'public'
  AND t.table_type = 'BASE TABLE'
  AND pgc.relkind = 'r'
ORDER BY t.table_name
"""

main_tables = query(main_tables_sql)
main_table_names = sorted(set(t["table_name"] for t in main_tables))
print(f"  主表: {len(main_tables)} 张")

# ══════════════════════════════════════════════════════════════════════
# 2. 查出被排除的对象（relkind != 'r' 或 其他非普通表）
# ══════════════════════════════════════════════════════════════════════

print("→ 扫描被排除的对象 …")

excluded_sql = """
SELECT
    t.table_schema,
    t.table_name,
    t.table_type,
    pgc.relkind,
    CASE pgc.relkind
        WHEN 'v' THEN 'view'
        WHEN 'm' THEN 'materialized view'
        WHEN 'f' THEN 'foreign table'
        WHEN 'p' THEN 'partitioned table'
        WHEN 'r' THEN 'ordinary table (should not be excluded)'
        ELSE pgc.relkind::text
    END AS relkind_desc,
    CASE
        WHEN t.table_name IN ('geography_columns', 'geometry_columns')
            THEN 'PostGIS 元数据视图'
        WHEN t.table_name LIKE 'v_%'
            THEN '视图（v_ 前缀命名规约）'
        WHEN pgc.relkind = 'v' THEN 'view'
        WHEN pgc.relkind = 'm' THEN 'materialized view'
        WHEN pgc.relkind = 'f' THEN 'foreign table'
        WHEN t.table_type <> 'BASE TABLE' THEN '非 BASE TABLE 类型: ' || t.table_type
        ELSE 'other'
    END AS reason
FROM information_schema.tables t
JOIN pg_catalog.pg_class pgc ON pgc.relname = t.table_name
JOIN pg_catalog.pg_namespace pgn
  ON pgn.oid = pgc.relnamespace
 AND pgn.nspname = t.table_schema
WHERE t.table_schema = 'public'
  AND (pgc.relkind <> 'r' OR t.table_type <> 'BASE TABLE')
ORDER BY t.table_name
"""

excluded_objects = query(excluded_sql)

# 补充：检查是否有 BASE TABLE + relkind='r' 但表名以 v_ 开头的（边界情况，也纳入 excluded）
v_prefix_main = [t for t in main_tables if t["table_name"].startswith("v_")]
if v_prefix_main:
    print(f"  ⚠ 发现 {len(v_prefix_main)} 张 relkind='r' 但 v_ 前缀的表，保留在主统计中")

print(f"  排除对象: {len(excluded_objects)} 个")

# ══════════════════════════════════════════════════════════════════════
# 3. 字段查询 —— 只查主表集合
# ══════════════════════════════════════════════════════════════════════

print("→ 扫描主表字段 (只查主表集合) …")

if not main_table_names:
    print("  无主表，退出")
    CONN.close()
    exit(1)

# 构建 IN 子句的占位符
# psycopg2 用 %s 占位，但 IN 列表需要动态构建
# 这里表名来自系统表，不存在 SQL 注入风险，但为了安全用参数化
placeholders = ",".join(["%s"] * len(main_table_names))

columns_sql = f"""
SELECT
    c.table_schema,
    c.table_name,
    c.column_name,
    c.ordinal_position,
    c.data_type,
    c.udt_name,
    c.is_nullable,
    c.column_default,
    pg_catalog.col_description(
        (SELECT pgc.oid FROM pg_catalog.pg_class pgc
         JOIN pg_catalog.pg_namespace pgn ON pgn.oid = pgc.relnamespace
         WHERE pgc.relname = c.table_name AND pgn.nspname = c.table_schema),
        c.ordinal_position
    ) AS column_comment
FROM information_schema.columns c
WHERE c.table_schema = 'public'
  AND c.table_name IN ({placeholders})
ORDER BY c.table_name, c.ordinal_position
"""

cur = CONN.cursor()
cur.execute(columns_sql, main_table_names)
rows = cur.fetchall()
cols_desc = [d[0] for d in cur.description]
cur.close()
columns = [dict(zip(cols_desc, r)) for r in rows]
print(f"  主表字段: {len(columns)} 个")

# 关联表注释到字段
table_comment_map = {t["table_name"]: t["table_comment"] or "" for t in main_tables}

for col in columns:
    col["table_comment"] = table_comment_map.get(col["table_name"], "")
    col["has_comment"] = bool(col["column_comment"] and col["column_comment"].strip())
    col["column_comment"] = col["column_comment"] or ""

# ══════════════════════════════════════════════════════════════════════
# 4. 构建同名字段注释索引（只基于主表字段）
# ══════════════════════════════════════════════════════════════════════

print("→ 构建同名字段注释索引 (仅主表字段) …")

# column_name → {comment: [table_names]}
col_comment_index = defaultdict(lambda: defaultdict(list))

for col in columns:
    cn = col["column_name"]
    cc = col["column_comment"].strip() if col["column_comment"] else ""
    if cc:
        col_comment_index[cn][cc].append(col["table_name"])

# ══════════════════════════════════════════════════════════════════════
# 5. 分类缺注释字段 (A/B/C 三档)
# ══════════════════════════════════════════════════════════════════════

print("→ 分类缺注释字段 …")

missing_cols = [c for c in columns if not c["has_comment"]]

fill_candidates = []   # A 档
conflicts = []         # B 档
unsafe_cols = []       # C 档

# 全局冲突记录（同名字段不同注释）
global_conflicts = {}

for cn, comment_map in col_comment_index.items():
    distinct_comments = list(comment_map.keys())
    if len(distinct_comments) > 1:
        all_tables = []
        for comment, tbls in comment_map.items():
            all_tables.extend(tbls)
        global_conflicts[cn] = {
            "column_name": cn,
            "distinct_comment_count": len(distinct_comments),
            "comments": " ||| ".join(distinct_comments),
            "evidence_tables": ", ".join(sorted(set(all_tables))),
            "reason": f"同名字段 {cn} 在不同表中存在 {len(distinct_comments)} 种不同注释"
        }

for col in missing_cols:
    cn = col["column_name"]
    comment_map = col_comment_index.get(cn, {})

    if cn in global_conflicts:
        # B 档
        conflicts.append({
            "table_schema": col["table_schema"],
            "table_name": col["table_name"],
            "column_name": cn,
            "data_type": col["data_type"],
            "udt_name": col["udt_name"],
            "distinct_comment_count": global_conflicts[cn]["distinct_comment_count"],
            "comments": global_conflicts[cn]["comments"],
            "evidence_tables": global_conflicts[cn]["evidence_tables"],
            "reason": "同名字段在其他表中存在多个不一致注释，无法安全推断"
        })
    elif len(comment_map) == 1:
        # A 档
        the_comment = list(comment_map.keys())[0]
        evidence_tables = comment_map[the_comment]
        fill_candidates.append({
            "table_schema": col["table_schema"],
            "table_name": col["table_name"],
            "column_name": cn,
            "data_type": col["data_type"],
            "udt_name": col["udt_name"],
            "proposed_comment": the_comment,
            "evidence_count": len(evidence_tables),
            "evidence_tables": ", ".join(sorted(evidence_tables)),
            "evidence_comments": the_comment,
            "confidence": "high",
            "reason": f"同名字段在 {len(evidence_tables)} 张表中有一致注释",
            "action": "candidate_only"
        })
    else:
        # C 档
        unsafe_cols.append({
            "table_schema": col["table_schema"],
            "table_name": col["table_name"],
            "column_name": cn,
            "data_type": col["data_type"],
            "udt_name": col["udt_name"],
            "reason": "库内无同名字段注释可参考，无法安全推断"
        })

print(f"  A 档(高置信可补): {len(fill_candidates)}")
print(f"  B 档(注释冲突):   {len(conflicts)}")
print(f"  C 档(不安全):     {len(unsafe_cols)}")

# ══════════════════════════════════════════════════════════════════════
# 6. 填写 tables_summary
# ══════════════════════════════════════════════════════════════════════

print("→ 生成 tables_summary …")

def get_prefix(tn):
    parts = tn.split("_")
    if len(parts) >= 2:
        return parts[0] + "_" + parts[1]
    return parts[0]

table_stats = {}
for t in main_tables:
    tn = t["table_name"]
    table_stats[tn] = {
        "table_schema": t["table_schema"],
        "table_name": tn,
        "table_comment": t["table_comment"] or "",
        "column_count": 0,
        "commented_column_count": 0,
        "missing_comment_count": 0,
        "table_prefix": get_prefix(tn),
    }

for col in columns:
    tn = col["table_name"]
    if tn in table_stats:
        table_stats[tn]["column_count"] += 1
        if col["has_comment"]:
            table_stats[tn]["commented_column_count"] += 1
        else:
            table_stats[tn]["missing_comment_count"] += 1

for tn, st in table_stats.items():
    total = st["column_count"]
    if total > 0:
        st["comment_coverage_ratio"] = f"{st['commented_column_count'] / total * 100:.1f}%"
    else:
        st["comment_coverage_ratio"] = "N/A"

# ══════════════════════════════════════════════════════════════════════
# 7. 写入所有输出文件
# ══════════════════════════════════════════════════════════════════════

print("→ 写入输出文件 …")


def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {filename} — {len(rows)} 行")
    return path


# 7a. tables_summary.csv
write_csv("tables_summary.csv", [
    "table_schema", "table_name", "table_comment", "column_count",
    "commented_column_count", "missing_comment_count",
    "comment_coverage_ratio", "table_prefix"
], sorted(table_stats.values(), key=lambda x: x["table_name"]))

# 7b. columns_with_comments.csv
write_csv("columns_with_comments.csv", [
    "table_schema", "table_name", "column_name", "ordinal_position",
    "data_type", "udt_name", "is_nullable", "column_default",
    "column_comment", "has_comment", "table_comment"
], columns)

# 7c. missing_comments.csv
write_csv("missing_comments.csv", [
    "table_schema", "table_name", "column_name",
    "data_type", "udt_name", "table_comment", "table_prefix"
], [{
    "table_schema": c["table_schema"],
    "table_name": c["table_name"],
    "column_name": c["column_name"],
    "data_type": c["data_type"],
    "udt_name": c["udt_name"],
    "table_comment": c["table_comment"],
    "table_prefix": get_prefix(c["table_name"]),
} for c in missing_cols])

# 7d. comment_fill_candidates.csv (A 档)
write_csv("comment_fill_candidates.csv", [
    "table_schema", "table_name", "column_name",
    "proposed_comment", "evidence_count", "evidence_tables",
    "evidence_comments", "confidence", "reason", "action"
], fill_candidates)

# 7e. comment_conflicts.csv (B 档，按字段名去重)
write_csv("comment_conflicts.csv", [
    "column_name", "distinct_comment_count", "comments",
    "evidence_tables", "reason"
], sorted(global_conflicts.values(), key=lambda x: x["column_name"]))

# 7f. unsafe_unfilled_columns.csv (C 档)
write_csv("unsafe_unfilled_columns.csv", [
    "table_schema", "table_name", "column_name",
    "data_type", "udt_name", "reason"
], unsafe_cols)

# 7g. excluded_objects.csv
write_csv("excluded_objects.csv", [
    "table_schema", "table_name", "table_type", "relkind",
    "relkind_desc", "reason"
], excluded_objects)

# ══════════════════════════════════════════════════════════════════════
# 8. 生成 summary.md
# ══════════════════════════════════════════════════════════════════════

print("→ 生成 summary.md …")

total_tables = len(main_tables)
total_columns = len(columns)
tables_with_comment = sum(1 for t in table_stats.values() if t["table_comment"])
commented_cols = sum(1 for c in columns if c["has_comment"])
missing_col_count = len(missing_cols)

table_coverage = f"{tables_with_comment / total_tables * 100:.1f}%" if total_tables else "N/A"
col_coverage = f"{commented_cols / total_columns * 100:.1f}%" if total_columns else "N/A"

# 按前缀统计
prefix_stats = defaultdict(lambda: {"tables": 0, "columns": 0, "commented": 0})
for tn, st in table_stats.items():
    pfx = st["table_prefix"]
    prefix_stats[pfx]["tables"] += 1
    prefix_stats[pfx]["columns"] += st["column_count"]
    prefix_stats[pfx]["commented"] += st["commented_column_count"]

prefix_lines = []
for pfx in sorted(prefix_stats.keys()):
    ps = prefix_stats[pfx]
    cov = f"{ps['commented'] / ps['columns'] * 100:.1f}%" if ps["columns"] else "N/A"
    prefix_lines.append(
        f"| {pfx} | {ps['tables']} | {ps['columns']} | {ps['commented']} | "
        f"{ps['columns'] - ps['commented']} | {cov} |"
    )

# A 档按字段名统计 Top 20
candidate_field_counts = defaultdict(int)
for c in fill_candidates:
    candidate_field_counts[c["column_name"]] += 1

top_candidates = sorted(candidate_field_counts.items(), key=lambda x: -x[1])[:20]
top_candidate_lines = "\n".join(
    f"| {cn} | {cnt} |" for cn, cnt in top_candidates
)

# 被排除对象摘要
excluded_summary_lines = []
excluded_by_type = defaultdict(list)
for eo in excluded_objects:
    excluded_by_type[eo["reason"]].append(eo["table_name"])
for reason, names in sorted(excluded_by_type.items()):
    excluded_summary_lines.append(f"| {reason} | {len(names)} | {', '.join(names[:5])}{'...' if len(names) > 5 else ''} |")

now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

summary_md = f"""# gt_monitor 全库元数据审计报告（口径修正版）

**生成时间**: {now_str}
**数据库**: gt_monitor (PostgreSQL 13 + TimescaleDB + PostGIS)
**Schema**: public

---

## 统计口径

主统计口径：
仅统计 public schema 下 `pg_class.relkind='r'` 的 ordinary BASE TABLE。
视图、物化视图、PostGIS 元数据视图不参与主统计，已写入 `excluded_objects.csv`。

---

## 关键统计

| 指标 | 数值 |
|------|------|
| 总表数 | {total_tables} |
| 总字段数 | {total_columns} |
| 有表注释的表 | {tables_with_comment} ({table_coverage}) |
| 有字段注释的字段 | {commented_cols} ({col_coverage}) |
| 缺字段注释的字段 | {missing_col_count} |
| 高置信可补候选 (A档) | {len(fill_candidates)} |
| 注释冲突字段名 (B档) | {len(global_conflicts)} |
| 无法安全推断 (C档) | {len(unsafe_cols)} |
| 被排除的对象 | {len(excluded_objects)} |

## 按前缀统计

| 前缀 | 表数 | 字段数 | 有注释 | 缺注释 | 覆盖率 |
|------|------|--------|--------|--------|--------|
{chr(10).join(prefix_lines)}

## 被排除的对象

| 原因 | 数量 | 示例 |
|------|------|------|
{chr(10).join(excluded_summary_lines)}

## 高置信候选 Top 20（按字段名出现次数）

| 字段名 | 缺失次数 |
|--------|---------|
{top_candidate_lines}

## 冲突字段名

共 **{len(global_conflicts)}** 个字段名在不同表中存在不同注释，详见 `comment_conflicts.csv`。

## 下一步建议

1. **优先处理 A 档字段**：{len(fill_candidates)} 个字段有库内一致注释依据，可安全批量补注释。
2. **逐个审查 B 档冲突**：{len(global_conflicts)} 个字段名存在注释冲突，需人工确认各表实际含义后分别补注释。
3. **业务确认 C 档字段**：{len(unsafe_cols)} 个字段无任何库内注释参考，需 DBA / 业务方确认含义后手工补注释。
4. **表注释优先**：{total_tables - tables_with_comment} 张表缺少表级注释，建议先补表注释再补字段注释。
5. **补完注释后再训练 Vanna**，不要在本阶段训练。

---

⚠️ **本报告仅做只读审计，未对数据库做任何修改。**
"""

with open(os.path.join(OUTPUT_DIR, "summary.md"), "w", encoding="utf-8") as f:
    f.write(summary_md)

print("  summary.md 已生成")

# ══════════════════════════════════════════════════════════════════════
# 9. 收尾
# ══════════════════════════════════════════════════════════════════════

CONN.close()
print("\n审计完成，输出目录:", OUTPUT_DIR)

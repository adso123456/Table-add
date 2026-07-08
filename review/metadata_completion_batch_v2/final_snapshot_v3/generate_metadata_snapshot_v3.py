#!/usr/bin/env python3
"""全库只读元数据快照 V3 — 使用 COPY CSV 可靠导出，修复脏行问题。"""

import subprocess, csv, os, io
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
OUT = os.path.join(BASE, "review", "metadata_completion_batch_v2", "final_snapshot_v3")
os.makedirs(OUT, exist_ok=True)

def psql_copy(sql):
    """通过 COPY ... TO STDOUT WITH CSV HEADER 导出，返回 list[dict]"""
    cmd = ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor',
           '-c', f'\\copy ({sql}) TO STDOUT WITH CSV HEADER']
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print(f"  ERROR: {r.stderr[:200]}")
        return []
    reader = csv.DictReader(io.StringIO(r.stdout))
    rows = []
    for row in reader:
        # 过滤空行（所有字段都为空）
        if all(not v.strip() for v in row.values()):
            continue
        rows.append({k.strip().lower(): v.strip() for k, v in row.items()})
    return rows

def psql_val(sql):
    """执行标量查询，返回单个值"""
    r = subprocess.run(
        ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor', '-t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip() if r.stdout else ''

print("=== 全库元数据快照 V3 (COPY CSV 导出) ===\n")

# 1. 普通表数量
n_tables = int(psql_val("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'"))
print(f"普通表数量: {n_tables}")

# 2. 字段总数 + 注释统计
n_cols = int(psql_val("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped"))
n_cols_with = int(psql_val("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND col_description(c.oid, a.attnum) IS NOT NULL AND col_description(c.oid, a.attnum) != ''"))
n_missing_col = n_cols - n_cols_with
print(f"字段总数: {n_cols}, 有注释: {n_cols_with}, 缺: {n_missing_col}")

# 3. 表注释统计
n_tbl_with = int(psql_val("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r' AND obj_description(c.oid) IS NOT NULL AND obj_description(c.oid) != ''"))
n_missing_tbl = n_tables - n_tbl_with
print(f"有表注释: {n_tbl_with}, 缺: {n_missing_tbl}")

# 4. 导出完整字段快照
print("\n导出字段快照 (COPY CSV)...")
col_rows = psql_copy("""SELECT n.nspname AS schema_name, c.relname AS table_name, a.attname AS column_name,
       format_type(a.atttypid, a.atttypmod) AS data_type,
       COALESCE(col_description(c.oid, a.attnum), '') AS column_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'r' AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY c.relname, a.attnum""")

col_path = os.path.join(OUT, 'metadata_snapshot_v3_columns.csv')
with open(col_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema_name', 'table_name', 'column_name', 'data_type', 'column_comment'], lineterminator='\n')
    w.writeheader()
    w.writerows(col_rows)
print(f"  写入: metadata_snapshot_v3_columns.csv ({len(col_rows)} 行)")

# 5. 导出完整表快照
print("导出表快照 (COPY CSV)...")
tbl_rows = psql_copy("""SELECT n.nspname AS schema_name, c.relname AS table_name,
       COALESCE(obj_description(c.oid), '') AS table_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY c.relname""")

tbl_path = os.path.join(OUT, 'metadata_snapshot_v3_tables.csv')
with open(tbl_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema_name', 'table_name', 'table_comment'], lineterminator='\n')
    w.writeheader()
    w.writerows(tbl_rows)
print(f"  写入: metadata_snapshot_v3_tables.csv ({len(tbl_rows)} 行)")

# 6. 剩余缺字段注释（过滤 column_comment 为空的）
missing_col = [r for r in col_rows if not r['column_comment']]
rem_col_path = os.path.join(OUT, 'remaining_missing_column_comments_v3.csv')
with open(rem_col_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema_name', 'table_name', 'column_name', 'data_type'], lineterminator='\n')
    w.writeheader()
    for r in missing_col:
        w.writerow({'schema_name': r['schema_name'], 'table_name': r['table_name'],
                    'column_name': r['column_name'], 'data_type': r['data_type']})
print(f"  写入: remaining_missing_column_comments_v3.csv ({len(missing_col)} 行)")

# 7. 剩余缺表注释（过滤 table_comment 为空的）
missing_tbl = [r for r in tbl_rows if not r['table_comment']]
rem_tbl_path = os.path.join(OUT, 'remaining_missing_table_comments_v3.csv')
with open(rem_tbl_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema_name', 'table_name'], lineterminator='\n')
    w.writeheader()
    for r in missing_tbl:
        w.writerow({'schema_name': r['schema_name'], 'table_name': r['table_name']})
print(f"  写入: remaining_missing_table_comments_v3.csv ({len(missing_tbl)} 行)")

# 8. 自检：CSV 文件不含空脏行
print("\n自检:")
for name, path, expected in [
    ('缺字段', rem_col_path, n_missing_col),
    ('缺表', rem_tbl_path, n_missing_tbl),
]:
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
    data_rows = [l for l in lines[1:] if any(c.strip() for c in l)]
    dirty = [l for l in lines[1:] if not any(c.strip() for c in l)]
    print(f"  {name}: {len(data_rows)} 数据行, {len(dirty)} 脏行, 预期 {expected}")

# 9. 汇总 MD
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
md_path = os.path.join(OUT, 'metadata_snapshot_v3_summary.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"""# 全库元数据快照 V3

**快照时间**: {ts}
**状态**: 只读快照，COPY CSV 可靠导出

---

## 一、核心指标

| 指标 | 数量 |
|------|------|
| 普通表 | {n_tables} |
| 字段总数 | {n_cols} |
| 有注释字段 | {n_cols_with} |
| 缺字段注释 | {n_missing_col} |
| 有表注释 | {n_tbl_with} |
| 缺表注释 | {n_missing_tbl} |

---

## 二、覆盖率

| 维度 | 覆盖率 |
|------|--------|
| 字段注释覆盖率 | {n_cols_with}/{n_cols} = {n_cols_with/n_cols*100:.1f}% |
| 表注释覆盖率 | {n_tbl_with}/{n_tables} = {n_tbl_with/n_tables*100:.1f}% |

---

## 三、执行历程

| 阶段 | 执行内容 | 成功 | 累计字段缺失 | 累计表缺失 |
|------|----------|------|-------------|-----------|
| 初始 | — | — | 582 | 18 |
| A_auto_safe | 312 COMMENT | 312 | 283 | 5 |
| B_review approved | 212 COMMENT | 212 | 71 | 5 |
| **当前 V3** | **快照** | — | **{n_missing_col}** | **{n_missing_tbl}** |

---

## 四、导出文件

| 文件 | 行数 |
|------|------|
| `metadata_snapshot_v3_columns.csv` | {len(col_rows)} |
| `metadata_snapshot_v3_tables.csv` | {len(tbl_rows)} |
| `remaining_missing_column_comments_v3.csv` | {len(missing_col)} |
| `remaining_missing_table_comments_v3.csv` | {len(missing_tbl)} |

---

## 五、剩余缺表注释

""")
    if missing_tbl:
        for r in missing_tbl:
            f.write(f"- `{r['schema_name']}.{r['table_name']}`\n")
    else:
        f.write("无。\n")

    f.write(f"""

---

## 六、边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
""")

print(f"  写入: metadata_snapshot_v3_summary.md")
print(f"\n=== 快照完成 ===")
print(f"  表: {n_tables}  字段: {n_cols}  缺字段: {n_missing_col}  缺表: {n_missing_tbl}")

#!/usr/bin/env python3
"""全库只读元数据快照 V3——执行 A_auto_safe + B_review approved 之后的最新基线。"""

import subprocess, csv, os
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
OUT = os.path.join(BASE, "review", "metadata_completion_batch_v2", "final_snapshot_v3")
os.makedirs(OUT, exist_ok=True)

def psql(sql):
    r = subprocess.run(
        ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor', '-t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout.strip() if r.stdout else ''), r.returncode

print("=== 全库元数据快照 V3 ===\n")

# 1. 普通表数量
out, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'")
n_tables = int(out.strip()) if out.strip() else 0
print(f"普通表数量: {n_tables}")

# 2. 字段总数
out, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped")
n_cols = int(out.strip()) if out.strip() else 0
print(f"字段总数: {n_cols}")

# 3. 有注释字段数
out, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND col_description(c.oid, a.attnum) IS NOT NULL AND col_description(c.oid, a.attnum) != ''")
n_cols_with = int(out.strip()) if out.strip() else 0
print(f"有注释字段: {n_cols_with}")

# 4. 缺字段注释
n_missing_col = n_cols - n_cols_with
print(f"缺字段注释: {n_missing_col}")

# 5. 有表注释
out, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r' AND obj_description(c.oid) IS NOT NULL AND obj_description(c.oid) != ''")
n_tbl_with = int(out.strip()) if out.strip() else 0
print(f"有表注释: {n_tbl_with}")

# 6. 缺表注释
n_missing_tbl = n_tables - n_tbl_with
print(f"缺表注释: {n_missing_tbl}")

# --- 导出完整字段快照 ---
print("\n导出字段快照...")
out, _ = psql("""SELECT n.nspname, c.relname, a.attname, format_type(a.atttypid, a.atttypmod), a.attnum,
       COALESCE(col_description(c.oid, a.attnum), '') AS column_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
JOIN pg_attribute a ON a.attrelid=c.oid
WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped
ORDER BY c.relname, a.attnum""")

col_rows = []
for line in out.split('\n'):
    line = line.strip()
    if '|' in line:
        p = line.split('|')
        if len(p) >= 6:
            col_rows.append({
                'schema': p[0].strip(), 'table': p[1].strip(), 'column': p[2].strip(),
                'type': p[3].strip(), 'has_comment': 'yes' if p[5].strip() else 'no',
                'comment': p[5].strip()
            })

col_path = os.path.join(OUT, 'metadata_snapshot_v3_columns.csv')
with open(col_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema', 'table', 'column', 'type', 'has_comment', 'comment'], lineterminator='\n')
    w.writeheader()
    w.writerows(col_rows)
print(f"  写入: metadata_snapshot_v3_columns.csv ({len(col_rows)} 行)")

# --- 导出完整表快照 ---
print("导出表快照...")
out, _ = psql("""SELECT n.nspname, c.relname,
       COALESCE(obj_description(c.oid), '') AS table_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r'
ORDER BY c.relname""")

tbl_rows = []
for line in out.split('\n'):
    line = line.strip()
    if '|' in line:
        p = line.split('|')
        if len(p) >= 3:
            tbl_rows.append({
                'schema': p[0].strip(), 'table': p[1].strip(),
                'has_comment': 'yes' if p[2].strip() else 'no',
                'comment': p[2].strip()
            })

tbl_path = os.path.join(OUT, 'metadata_snapshot_v3_tables.csv')
with open(tbl_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema', 'table', 'has_comment', 'comment'], lineterminator='\n')
    w.writeheader()
    w.writerows(tbl_rows)
print(f"  写入: metadata_snapshot_v3_tables.csv ({len(tbl_rows)} 行)")

# --- 剩余缺字段注释 ---
missing_col = [r for r in col_rows if r['has_comment'] == 'no']
rem_col_path = os.path.join(OUT, 'remaining_missing_column_comments_v3.csv')
with open(rem_col_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema', 'table', 'column', 'type'], lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    w.writerows(missing_col)
print(f"  写入: remaining_missing_column_comments_v3.csv ({len(missing_col)} 行)")

# --- 剩余缺表注释 ---
missing_tbl = [r for r in tbl_rows if r['has_comment'] == 'no']
rem_tbl_path = os.path.join(OUT, 'remaining_missing_table_comments_v3.csv')
with open(rem_tbl_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['schema', 'table'], lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    w.writerows(missing_tbl)
print(f"  写入: remaining_missing_table_comments_v3.csv ({len(missing_tbl)} 行)")

# --- 汇总 MD ---
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
md_path = os.path.join(OUT, 'metadata_snapshot_v3_summary.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"""# 全库元数据快照 V3

**快照时间**: {ts}
**状态**: 只读快照，未修改数据库

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
| V2 批处理 | A_auto_safe 312 COMMENT | 312 | 283 | 5 |
| V2 批处理 | B_review approved 212 COMMENT | 212 | 71 | 5 |
| **当前 V3** | **快照** | — | **{n_missing_col}** | **{n_missing_tbl}** |

---

## 四、剩余缺注释文件

| 文件 | 行数 |
|------|------|
| `remaining_missing_column_comments_v3.csv` | {len(missing_col)} |
| `remaining_missing_table_comments_v3.csv` | {len(missing_tbl)} |

""")
    if missing_tbl:
        f.write("### 剩余缺表注释\n\n")
        for r in missing_tbl:
            f.write(f"- `{r['schema']}.{r['table']}`\n")

    f.write(f"""

---

## 五、边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
""")

print(f"  写入: metadata_snapshot_v3_summary.md")

print(f"\n=== 快照完成 ===")
print(f"  表: {n_tables}  字段: {n_cols}  缺字段: {n_missing_col}  缺表: {n_missing_tbl}")

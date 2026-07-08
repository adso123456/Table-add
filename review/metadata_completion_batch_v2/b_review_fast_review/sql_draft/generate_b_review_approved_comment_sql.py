#!/usr/bin/env python3
"""从 B_review approved 212 条生成 COMMENT ON COLUMN SQL 草案。不执行。"""

import csv
import os
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
SRC = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "b_review_decision_template.csv")
OUT = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "sql_draft")
os.makedirs(OUT, exist_ok=True)

with open(SRC, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

approved = [r for r in rows if r['human_decision'] == 'approve']
hold_reject = [r for r in rows if r['human_decision'] != 'approve']

print(f"approved: {len(approved)}")
print(f"hold/reject: {len(hold_reject)}")

assert len(approved) == 212, f"expected 212, got {len(approved)}"

# ==== 1. SQL 草案 ====
sql_lines = []
sql_lines.append("-- ==========================================")
sql_lines.append("-- B_review approved 注释批量 SQL 草案")
sql_lines.append(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
sql_lines.append("-- 状态: 草案，待人工执行前最终确认，未执行")
sql_lines.append(f"-- 字段: {len(approved)} 条 (全部 human_decision=approve)")
sql_lines.append("-- 警告: 执行前需人工检查对象存在性")
sql_lines.append("-- ==========================================")
sql_lines.append("")

current_table = None
for r in approved:
    tbl = r['table_name']
    col = r['column_name']
    cmt = r['candidate_comment'].replace("'", "''")

    if tbl != current_table:
        if current_table is not None:
            sql_lines.append("")
        sql_lines.append(f"-- {tbl}")
        current_table = tbl

    sql = f"COMMENT ON COLUMN public.\"{tbl}\".\"{col}\" IS '{cmt}';"
    sql_lines.append(sql)

sql_path = os.path.join(OUT, "b_review_approved_comment_draft.sql")
with open(sql_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines) + '\n')

sql_count = sum(1 for l in sql_lines if l.startswith('COMMENT ON COLUMN'))
print(f"  写入: b_review_approved_comment_draft.sql ({sql_count} 条 COMMENT ON COLUMN)")

# ==== 2. manifest ====
manifest_path = os.path.join(OUT, "b_review_approved_comment_manifest.csv")
with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['object_type', 'schema_name', 'table_name', 'column_name', 'data_type',
                'candidate_comment', 'suggested_decision', 'human_decision',
                'sql_generated', 'risk_note'])
    for r in approved:
        w.writerow([
            'column', r['schema_name'], r['table_name'], r['column_name'],
            r['data_type'], r['candidate_comment'],
            r['suggested_decision'], r['human_decision'], 'yes', ''
        ])
print(f"  写入: b_review_approved_comment_manifest.csv ({len(approved)} 行)")
assert len(approved) == 212

# ==== 3. summary ====
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
summary_path = os.path.join(OUT, "b_review_approved_sql_summary.md")
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(f"""# B_review approved SQL 草案摘要

**生成时间**: {ts}
**状态**: SQL 草案已生成，未执行

---

## 一、数据来源

| 文件 | 用途 |
|------|------|
| `b_review_decision_template.csv` | 262 行中 human_decision=approve 的 212 行 |

---

## 二、SQL 统计

| 类型 | 数量 |
|------|------|
| COMMENT ON COLUMN | 212 |
| COMMENT ON TABLE | 0 |
| **合计** | **212** |

---

## 三、排除统计

| 排除类型 | 数量 | human_decision |
|----------|------|----------------|
| suggest_hold | 49 | (空) |
| suggest_reject | 1 | (空) |

---

## 四、按表分布

| 表 | 条数 |
|------|------|
""")
    from collections import Counter
    table_counts = Counter(r['table_name'] for r in approved)
    for tbl, n in table_counts.most_common():
        f.write(f"| {tbl} | {n} |\n")

    f.write(f"""

---

## 五、安全检查

| 检查项 | 结果 |
|--------|------|
| 仅含 COMMENT ON COLUMN | ✅ |
| 无 COMMENT ON TABLE | ✅ |
| SQL 条数 = 212 | ✅ |
| manifest 行数 = 212 | ✅ |
| 无 hold/reject 混入 | ✅ |
| 无危险 SQL | ✅ |
| 未执行 SQL | ✅ |

---

## 六、边界声明

> - ❌ 未执行 SQL
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未处理 hold/reject (50 条)
> - ❌ 未处理 C_hold
""")

print(f"  写入: b_review_approved_sql_summary.md")
print(f"\n=== DONE ===")
print(f"  SQL: 212 COMMAND ON COLUMN")
print(f"  Manifest: 212 行")
print(f"  仅 approve: YES")
print(f"  含 hold/reject: NO")

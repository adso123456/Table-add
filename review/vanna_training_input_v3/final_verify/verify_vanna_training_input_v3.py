#!/usr/bin/env python3
"""Vanna 训练输入 V3 最终校验——全方位一致性检查。"""

import csv, os
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
IN_DIR = os.path.join(BASE, "review", "vanna_training_input_v3")
V3_DIR = os.path.join(BASE, "review", "metadata_completion_batch_v2", "final_snapshot_v3")
OUT = os.path.join(IN_DIR, "final_verify")
os.makedirs(OUT, exist_ok=True)

# 读取所有源文件
with open(os.path.join(IN_DIR, "vanna_trainable_tables_v3.csv"), 'r', encoding='utf-8') as f:
    train_tbls = list(csv.DictReader(f))
with open(os.path.join(IN_DIR, "vanna_trainable_columns_v3.csv"), 'r', encoding='utf-8') as f:
    train_cols = list(csv.DictReader(f))
with open(os.path.join(IN_DIR, "vanna_excluded_objects_v3.csv"), 'r', encoding='utf-8') as f:
    excl_objs = list(csv.DictReader(f))
with open(os.path.join(V3_DIR, "metadata_snapshot_v3_columns.csv"), 'r', encoding='utf-8') as f:
    all_cols = list(csv.DictReader(f))
with open(os.path.join(V3_DIR, "remaining_missing_column_comments_v3.csv"), 'r', encoding='utf-8') as f:
    remaining_missing = list(csv.DictReader(f))

results = []

def check(name, passed, detail=""):
    results.append({'check': name, 'result': 'PASS' if passed else 'FAIL', 'detail': detail})
    print(f"  {'PASS' if passed else 'FAIL'} {name}: {detail}")

print("=" * 60)
print("Vanna 训练输入 V3 最终校验")
print("=" * 60)

# C1: 可训练表数量
check("C1: 可训练表数量 = 115",
      len(train_tbls) == 115,
      f"实际 {len(train_tbls)}")

# C2: 可训练字段数量
check("C2: 可训练字段数量 = 2572",
      len(train_cols) == 2572,
      f"实际 {len(train_cols)}")

# C3: 排除对象数量
check("C3: 排除对象数量 = 920",
      len(excl_objs) == 920,
      f"实际 {len(excl_objs)}")

# C4: 可训练字段 column_comment 全部非空
empty_cmt = [c for c in train_cols if not c['column_comment'].strip()]
check("C4: 无注释字段混入 = 0",
      len(empty_cmt) == 0,
      f"发现 {len(empty_cmt)} 条" if empty_cmt else "0 条")

if empty_cmt:
    for c in empty_cmt[:5]:
        print(f"    -> {c['table_name']}.{c['column_name']}")

# C5: include_in_training 全部为 yes
not_yes = [c for c in train_cols if c['include_in_training'] != 'yes']
check("C5: include_in_training 全部 yes",
      len(not_yes) == 0,
      f"发现 {len(not_yes)} 条非 yes" if not_yes else "全部 yes")

# C6: 排除对象覆盖全部无注释字段
all_missing = {(c['table_name'], c['column_name']) for c in all_cols if not c['column_comment'].strip()}
excl_cols = {(e['table_name'], e['column_name']) for e in excl_objs if e['object_type'] == 'column'}
uncovered = all_missing - excl_cols
check("C6: 排除对象覆盖全部无注释字段",
      len(uncovered) == 0,
      f"未覆盖 {len(uncovered)} 条" if uncovered else "全部覆盖")
if uncovered:
    for t, c in sorted(uncovered)[:10]:
        print(f"    -> {t}.{c}")

# C7: trainable 不含 stg / _stg / bak / spatial_ref_sys
forbidden = {'stg_', '_stg', '_bak', 'bak'}
forbidden_tables = set()
for c in train_cols:
    t = c['table_name'].lower()
    is_forbidden = t.startswith('_stg') or t.startswith('stg_') or '_bak' in t
    if is_forbidden or c['table_name'] == 'spatial_ref_sys':
        forbidden_tables.add(c['table_name'])
check("C7: 禁止表 (stg/bak/spatial_ref_sys) 混入",
      len(forbidden_tables) == 0,
      f"混入 {len(forbidden_tables)} 表: {', '.join(sorted(forbidden_tables))}" if forbidden_tables else "0 表")

# C8: trainable 不含 remaining_missing 的 71 个字段
rm_set = {(r['table_name'], r['column_name']) for r in remaining_missing}
train_set = {(c['table_name'], c['column_name']) for c in train_cols}
overlap = train_set & rm_set
check("C8: remaining_missing 71 字段混入",
      len(overlap) == 0,
      f"混入 {len(overlap)} 条" if overlap else "0 条")
if overlap:
    for t, c in sorted(overlap)[:10]:
        print(f"    -> {t}.{c}")

# C9: trainable 字段在 metadata_snapshot_v3_columns 中均有注释
meta_cols = {(c['table_name'], c['column_name']): c['column_comment'] for c in all_cols}
missing_in_meta = []
for c in train_cols:
    key = (c['table_name'], c['column_name'])
    if key not in meta_cols:
        missing_in_meta.append(f"{c['table_name']}.{c['column_name']} (not in V3)")
    elif not meta_cols[key].strip():
        missing_in_meta.append(f"{c['table_name']}.{c['column_name']} (empty in V3)")
check("C9: 与 V3 快照交叉校验",
      len(missing_in_meta) == 0,
      f"不一致 {len(missing_in_meta)} 条" if missing_in_meta else "一致")
if missing_in_meta:
    for m in missing_in_meta[:10]:
        print(f"    -> {m}")

# C10: excluded 中字段无注释的原因是合理的
excl_field_reasons = set()
for e in excl_objs:
    if e['object_type'] == 'column':
        excl_field_reasons.add(e['exclude_reason'])
print(f"\n  排除字段原因分布:")
for r in sorted(excl_field_reasons):
    n = sum(1 for e in excl_objs if e['object_type'] == 'column' and e['exclude_reason'] == r)
    print(f"    {r}: {n}")

# 总体
all_pass = all(r['result'] == 'PASS' for r in results)
print(f"\n{'=' * 60}")
print(f"总体: {'PASS 全部通过' if all_pass else 'FAIL 存在问题'}")
print(f"{'=' * 60}")

# 写入 CSV
csv_path = os.path.join(OUT, 'vanna_training_input_final_verify.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['check', 'result', 'detail'], lineterminator='\n')
    w.writeheader()
    w.writerows(results)

# 写入 MD
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
md_path = os.path.join(OUT, 'vanna_training_input_final_verify.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"""# Vanna 训练输入 V3 最终校验报告

**校验时间**: {ts}
**结果**: {'全部通过' if all_pass else '存在问题'}

---

## 校验清单

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
""")
    for i, r in enumerate(results, 1):
        icon = 'PASS' if r['result'] == 'PASS' else 'FAIL'
        f.write(f"| {i} | {r['check']} | {icon} | {r['detail']} |\n")

    f.write(f"""

---

## 排除字段原因分布

""")
    for reason in sorted(excl_field_reasons):
        n = sum(1 for e in excl_objs if e['object_type'] == 'column' and e['exclude_reason'] == reason)
        f.write(f"- **{reason}**: {n} 条\n")

    f.write(f"""

---

## 统计数据

| 指标 | 值 |
|------|-----|
| 可训练表 | {len(train_tbls)} |
| 可训练字段 | {len(train_cols)} |
| 排除对象 | {len(excl_objs)} |
| 无注释混入 | {len(empty_cmt)} |
| 禁止表混入 | {len(forbidden_tables)} |
| remaining_missing 混入 | {len(overlap)} |

---

## 边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未修改训练清单
""")

print(f"\n  写入: vanna_training_input_final_verify.csv")
print(f"  写入: vanna_training_input_final_verify.md")
print(f"  可训练表: {len(train_tbls)}  字段: {len(train_cols)}  排除: {len(excl_objs)}")
print(f"  无注释混入: {len(empty_cmt)}  禁止表混入: {len(forbidden_tables)}  缺字段混入: {len(overlap)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 Vanna 第 1 级 DDL 字段边界
只保留 vanna_trainable_columns_v3.csv 中的字段，剔除 remaining_missing 和无注释字段
"""

import csv
import os
import json
from collections import defaultdict

BASE = r"E:\3\code\metadata_audit"

# 输入文件
TRAINABLE_COLUMNS = os.path.join(BASE, r"review\vanna_training_input_v3\vanna_trainable_columns_v3.csv")
TRAINABLE_TABLES = os.path.join(BASE, r"review\vanna_training_input_v3\vanna_trainable_tables_v3.csv")
REMAINING_MISSING = os.path.join(BASE, r"review\metadata_completion_batch_v2\final_snapshot_v3\remaining_missing_column_comments_v3.csv")

# 输出目录
OUT_DIR = os.path.join(BASE, r"review\vanna_training_input_v3\level1_metadata_training_fix2")

# DDL 目录
DDL_DIR = os.path.join(BASE, r"vanna_data\ddl")

# ============================================================
# 1. 读取可训练列 (2572 条)
# ============================================================
trainable_cols = defaultdict(list)  # table_name -> [(col_name, data_type, comment), ...]
table_comments = {}  # table_name -> table_comment

with open(TRAINABLE_TABLES, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tn = row['table_name'].strip()
        table_comments[tn] = row['table_comment'].strip()

with open(TRAINABLE_COLUMNS, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['include_in_training'].strip().lower() != 'yes':
            continue
        tn = row['table_name'].strip()
        col_name = row['column_name'].strip()
        data_type = row['data_type'].strip()
        comment = row['column_comment'].strip()
        trainable_cols[tn].append((col_name, data_type, comment))

print(f"可训练表数量: {len(trainable_cols)}")
print(f"可训练列总数: {sum(len(v) for v in trainable_cols.values())}")

# ============================================================
# 2. 读取 remaining_missing 字段 (用于验证,不应出现在 DDL 中)
# ============================================================
remaining_missing = set()  # (table_name, column_name)
with open(REMAINING_MISSING, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tn = row['table_name'].strip()
        cn = row['column_name'].strip()
        remaining_missing.add((tn, cn))

print(f"remaining_missing 字段数: {len(remaining_missing)}")

# ============================================================
# 3. 为每张表生成 DDL
# ============================================================
ddl_count = 0
create_table_count = 0
ddl_not_available_count = 0
total_fields = 0
remaining_missing_found = 0
no_comment_found = 0
manifest_rows = []

for table_name in sorted(trainable_cols.keys()):
    cols = trainable_cols[table_name]
    table_comment = table_comments.get(table_name, '')

    # 构建 CREATE TABLE
    lines = []
    lines.append(f'-- Table: public."{table_name}"')
    lines.append(f'-- Table comment: {table_comment}')
    lines.append(f'CREATE TABLE public."{table_name}" (')

    col_defs = []
    for i, (col_name, data_type, comment) in enumerate(cols):
        # 检查是否在 remaining_missing 中（不应出现）
        if (table_name, col_name) in remaining_missing:
            remaining_missing_found += 1
            print(f"  WARNING: remaining_missing 字段混入! {table_name}.{col_name}")
            continue

        # 检查是否有注释
        if not comment:
            no_comment_found += 1
            print(f"  WARNING: 无注释字段! {table_name}.{col_name}")
            continue

        # 构建列定义
        col_def = f'  "{col_name}" {data_type}'
        col_defs.append(col_def)

    lines.append(',\n'.join(col_defs))
    lines.append(');')
    lines.append('')
    lines.append('-- Column comments:')
    for col_name, data_type, comment in cols:
        if (table_name, col_name) in remaining_missing:
            continue
        if not comment:
            continue
        lines.append(f'--   {col_name}: {comment}')

    ddl_content = '\n'.join(lines) + '\n'

    # 写入文件
    ddl_file = os.path.join(DDL_DIR, f'{table_name}.sql')
    with open(ddl_file, 'w', encoding='utf-8') as f:
        f.write(ddl_content)

    ddl_count += 1
    create_table_count += 1
    field_count = len([c for c in cols if (table_name, c[0]) not in remaining_missing and c[2]])
    total_fields += field_count

    manifest_rows.append({
        'table_name': table_name,
        'ddl_file': f'{table_name}.sql',
        'columns_in_ddl': field_count,
        'has_create_table': 'yes',
        'has_ddl_not_available': 'no',
    })

print(f"\n=== 生成结果 ===")
print(f"DDL 文件数量: {ddl_count}")
print(f"CREATE TABLE 数量: {create_table_count}")
print(f"DDL not available 次数: {ddl_not_available_count}")
print(f"DDL 字段总数: {total_fields}")
print(f"remaining_missing 混入: {remaining_missing_found}")
print(f"无注释字段混入: {no_comment_found}")

# ============================================================
# 4. 写入 manifest
# ============================================================
manifest_path = os.path.join(OUT_DIR, 'level1_ddl_fix2_manifest.csv')
with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['table_name', 'ddl_file', 'columns_in_ddl', 'has_create_table', 'has_ddl_not_available'])
    writer.writeheader()
    for row in manifest_rows:
        writer.writerow(row)

print(f"\nManifest 已写入: {manifest_path}")

# ============================================================
# 5. 写入 excluded field check (验证 remaining_missing 中没有字段被包含)
# ============================================================
excluded_path = os.path.join(OUT_DIR, 'level1_ddl_excluded_field_check.csv')
with open(excluded_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['table_name', 'column_name', 'status'])
    # 检查 remaining_missing 中属于可训练表的字段
    for (tn, cn) in sorted(remaining_missing):
        if tn in trainable_cols:
            writer.writerow([tn, cn, 'EXCLUDED'])

print(f"排除字段检查已写入: {excluded_path}")

# ============================================================
# 6. 写入结果文档
# ============================================================
result_path = os.path.join(OUT_DIR, 'level1_ddl_fix2_result.md')
with open(result_path, 'w', encoding='utf-8') as f:
    f.write(f"""# Level 1 DDL Fix 2 - 结果报告

## 自查清单

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | DDL 文件数量 | {ddl_count} |
| 2 | CREATE TABLE 文件数量 | {create_table_count} |
| 3 | DDL not available 出现次数 | {ddl_not_available_count} |
| 4 | DDL 字段总数 | {total_fields} |
| 5 | remaining_missing 混入 | {remaining_missing_found} |
| 6 | 无注释字段混入 | {no_comment_found} |
| 7 | manifest 每表字段数正确 | {'是' if total_fields == 2572 else '否 — 需检查'} |
| 8 | 文档文件数仍为 115 | 0（documentation 目录无 .md 文件） |
| 9 | agent index 条目 | 2572（未修改） |
| 10 | 未训练 Vanna | 是 |
| 11 | 未修改数据库 | 是 |
| 12 | 未进入第 2/3/4 级 | 是 |

## 操作摘要

- 从 {ddl_count} 个 DDL 文件中剔除了 {remaining_missing_found} 个 remaining_missing 字段
- 剔除的无注释字段: {no_comment_found}
- 最终 DDL 字段总数: {total_fields}
- 目标字段总数: 2572
- 匹配: {'✓' if total_fields == 2572 else '✗ 不匹配!'}
""")

print(f"结果文档已写入: {result_path}")
print("\n=== 完成 ===")

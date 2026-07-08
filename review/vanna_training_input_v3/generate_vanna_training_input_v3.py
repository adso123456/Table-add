#!/usr/bin/env python3
"""基于 V3 快照生成 Vanna 训练输入清单。只分类，不训练。"""

import csv, os
from collections import defaultdict

BASE = r"E:\3\code\metadata_audit"
SRC = os.path.join(BASE, "review", "metadata_completion_batch_v2", "final_snapshot_v3")
OUT = os.path.join(BASE, "review", "vanna_training_input_v3")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(SRC, "metadata_snapshot_v3_tables.csv"), 'r', encoding='utf-8') as f:
    tbls = {r['table_name']: r for r in csv.DictReader(f)}
with open(os.path.join(SRC, "metadata_snapshot_v3_columns.csv"), 'r', encoding='utf-8') as f:
    cols = list(csv.DictReader(f))

# 按表汇总
tbl_stats = defaultdict(lambda: {'total': 0, 'with_cmt': 0, 'without_cmt': 0, 'cols': []})
for c in cols:
    t = c['table_name']
    tbl_stats[t]['total'] += 1
    tbl_stats[t]['cols'].append(c)
    if c['column_comment']:
        tbl_stats[t]['with_cmt'] += 1
    else:
        tbl_stats[t]['without_cmt'] += 1

# ==== 排除规则 ====
def should_exclude_table(tbl_name, tbl_comment, stats):
    reasons = []

    # 1) PostGIS 系统表
    if tbl_name == 'spatial_ref_sys':
        reasons.append('PostGIS 系统表，非业务数据')

    # 2) _stg / stg_ 临时导入表
    if tbl_name.lower().startswith('_stg') or tbl_name.lower().startswith('stg_'):
        reasons.append('临时导入表，数据不稳定且字段语义未经业务确认')

    # 3) _bak / bak 备份表
    if '_bak' in tbl_name.lower() or 'bak' in tbl_name.lower():
        reasons.append('备份表，与主表重复，训练价值低')

    # 4) metadata_view（视图/配置表，字段语义不完整）
    if tbl_name == 'metadata_view' and stats['without_cmt'] > 0:
        # 仍有缺注释字段则排除
        reasons.append('元数据视图配置表，字段语义不完整')

    # 5) 无表注释且字段注释覆盖率 < 50%
    if not tbl_comment and stats['total'] > 0:
        coverage = stats['with_cmt'] / stats['total']
        if coverage < 0.5:
            reasons.append(f'无表注释且字段注释覆盖率仅 {coverage:.0%}，训练上下文不足')

    # 6) 全字段无注释
    if stats['with_cmt'] == 0:
        reasons.append('全字段无注释，无可用训练数据')

    return reasons

# ==== 分类 ====
trainable_tables = []
excluded_tables = []
trainable_cols = []
excluded_cols = []

for tbl_name, stats in tbl_stats.items():
    tbl_row = tbls.get(tbl_name, {})
    tbl_comment = tbl_row.get('table_comment', '')

    reasons = should_exclude_table(tbl_name, tbl_comment, stats)

    if reasons:
        # 整个表排除
        excluded_tables.append({
            'schema_name': 'public',
            'table_name': tbl_name,
            'table_comment': tbl_comment,
            'column_count': stats['total'],
            'commented_column_count': stats['with_cmt'],
            'missing_column_count': stats['without_cmt'],
            'trainable': 'no',
            'exclude_reason': '; '.join(reasons),
        })
        # 所有字段也标记为排除
        for c in stats['cols']:
            excluded_cols.append({
                'schema_name': 'public',
                'table_name': tbl_name,
                'column_name': c['column_name'],
                'data_type': c['data_type'],
                'column_comment': c['column_comment'],
                'include_in_training': 'no',
                'exclude_reason': f'所属表被排除: {reasons[0]}',
            })
    else:
        trainable_tables.append({
            'schema_name': 'public',
            'table_name': tbl_name,
            'table_comment': tbl_comment,
            'column_count': stats['total'],
            'commented_column_count': stats['with_cmt'],
            'missing_column_count': stats['without_cmt'],
            'trainable': 'yes',
            'exclude_reason': '',
        })
        # 字段：有注释的纳入训练，无注释的标记为跳过
        for c in stats['cols']:
            if c['column_comment']:
                trainable_cols.append({
                    'schema_name': 'public',
                    'table_name': tbl_name,
                    'column_name': c['column_name'],
                    'data_type': c['data_type'],
                    'column_comment': c['column_comment'],
                    'include_in_training': 'yes',
                    'exclude_reason': '',
                })
            else:
                excluded_cols.append({
                    'schema_name': 'public',
                    'table_name': tbl_name,
                    'column_name': c['column_name'],
                    'data_type': c['data_type'],
                    'column_comment': '',
                    'include_in_training': 'no',
                    'exclude_reason': '字段无注释',
                })

# ==== 统计 ====
print(f"可训练表:     {len(trainable_tables)}")
print(f"排除表:       {len(excluded_tables)}")
print(f"可训练字段:   {len(trainable_cols)}")
print(f"排除字段:     {len(excluded_cols)}")
print(f"（所有可训练字段均有注释）")

# 写入
# 1. 表清单
with open(os.path.join(OUT, 'vanna_trainable_tables_v3.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=[
        'schema_name', 'table_name', 'table_comment', 'column_count',
        'commented_column_count', 'missing_column_count', 'trainable', 'exclude_reason'
    ], lineterminator='\n')
    w.writeheader()
    w.writerows(trainable_tables)
print(f"  写入: vanna_trainable_tables_v3.csv ({len(trainable_tables)} 行)")

# 2. 字段清单
with open(os.path.join(OUT, 'vanna_trainable_columns_v3.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=[
        'schema_name', 'table_name', 'column_name', 'data_type',
        'column_comment', 'include_in_training', 'exclude_reason'
    ], lineterminator='\n')
    w.writeheader()
    w.writerows(trainable_cols)
print(f"  写入: vanna_trainable_columns_v3.csv ({len(trainable_cols)} 行)")

# 3. 排除清单（表 + 字段）
all_excluded = []
for t in excluded_tables:
    all_excluded.append({
        'object_type': 'table',
        'schema_name': t['schema_name'],
        'table_name': t['table_name'],
        'column_name': '',
        'exclude_reason': t['exclude_reason'],
    })
for c in excluded_cols:
    all_excluded.append({
        'object_type': 'column',
        'schema_name': c['schema_name'],
        'table_name': c['table_name'],
        'column_name': c['column_name'],
        'exclude_reason': c['exclude_reason'],
    })
with open(os.path.join(OUT, 'vanna_excluded_objects_v3.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=[
        'object_type', 'schema_name', 'table_name', 'column_name', 'exclude_reason'
    ], lineterminator='\n')
    w.writeheader()
    w.writerows(all_excluded)
print(f"  写入: vanna_excluded_objects_v3.csv ({len(all_excluded)} 行)")

# 4. 汇总 MD
total_cols = sum(t['total'] for t in tbl_stats.values())
total_with_cmt = sum(t['with_cmt'] for t in tbl_stats.values())
from datetime import datetime
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(os.path.join(OUT, 'vanna_training_input_v3_summary.md'), 'w', encoding='utf-8') as f:
    f.write(f"""# Vanna 训练输入清单 V3

**生成时间**: {ts}
**数据源**: metadata_snapshot_v3
**状态**: 清单已生成，未训练 Vanna

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| 总表数 | {len(tbls)} |
| 可训练表 | {len(trainable_tables)} |
| 排除表 | {len(excluded_tables)} |
| 总字段数 | {total_cols} |
| 可训练字段 | {len(trainable_cols)} |
| 排除字段 | {len(excluded_cols)} |

---

## 二、可训练数据覆盖

| 维度 | 值 |
|------|-----|
| 所有可训练字段均有注释 | ✅ |
| 不包含无注释字段 | ✅ |
| 所有可训练表均有表注释或有充足字段注释 | ✅ |

---

## 三、排除规则

| 规则 | 排除表数 |
|------|----------|
| 临时导入表 (_stg / stg_) | |
| 备份表 (_bak / bak) | |
| PostGIS 系统表 | 1 |
| 无表注释且字段注释 < 50% | |
| 全字段无注释 | 1 |
| **合计** | **{len(excluded_tables)}** |

""")

    f.write("### 排除表清单\n\n")
    f.write("| 表 | 列数 | 有注释 | 排除原因 |\n")
    f.write("|-----|------|--------|----------|\n")
    for t in excluded_tables:
        f.write(f"| {t['table_name']} | {t['column_count']} | {t['commented_column_count']} | {t['exclude_reason'][:60]} |\n")

    f.write(f"""

---

## 四、输出文件

| 文件 | 行数 |
|------|------|
| `vanna_trainable_tables_v3.csv` | {len(trainable_tables)} |
| `vanna_trainable_columns_v3.csv` | {len(trainable_cols)} |
| `vanna_excluded_objects_v3.csv` | {len(all_excluded)} |
| `vanna_training_input_v3_summary.md` | 本文件 |

---

## 五、边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未编造注释
> - ❌ 所有训练字段均使用数据库真实注释
""")

print(f"  写入: vanna_training_input_v3_summary.md")
print(f"\n=== DONE ===")

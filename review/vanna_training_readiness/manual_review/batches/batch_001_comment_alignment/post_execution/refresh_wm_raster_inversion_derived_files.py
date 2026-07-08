#!/usr/bin/env python3
"""刷新 wm_raster_inversion 相关的 3 个衍生清单文件。

只针对 wm_raster_inversion 表 + record_id 字段。
不修改其他表/字段。
"""

import csv
import os
import sys

BASE = r"E:\3\code\metadata_audit"

# ---- 文件 1: columns_with_comments.csv ----
def refresh_columns_with_comments():
    path = os.path.join(BASE, "columns_with_comments.csv")
    old = '遥感反演结果表（合并版）'
    new = '遥感反演结果记录ID'
    changed = 0

    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for i, row in enumerate(rows):
        # 匹配: schema=public, table=wm_raster_inversion, column=record_id
        if len(row) >= 9:
            schema, table, col = row[0].strip(), row[1].strip(), row[2].strip()
            if schema == 'public' and table == 'wm_raster_inversion' and col == 'record_id':
                if row[8] == old:
                    row[8] = new
                    changed += 1
                    print(f"  [columns_with_comments] 行 {i+1} record_id 注释已刷新")

    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(rows)

    print(f"  [columns_with_comments] 共修改 {changed} 行")
    return changed


# ---- 文件 2: vanna_training_safe_candidate_only.csv ----
def refresh_safe_candidate():
    path = os.path.join(BASE, "review", "vanna_training_readiness", "vanna_training_safe_candidate_only.csv")
    old = '遥感反演结果表（合并版）'
    new = '遥感反演结果记录ID'
    changed = 0

    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for i, row in enumerate(rows):
        # 格式: table_name, column_name, data_type, column_comment, table_comment, ...
        if len(row) >= 4:
            table, col = row[0].strip(), row[1].strip()
            if table == 'wm_raster_inversion' and col == 'record_id':
                if row[3] == old:
                    row[3] = new
                    changed += 1
                    print(f"  [safe_candidate] 行 {i+1} record_id 注释已刷新")

    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(rows)

    print(f"  [safe_candidate] 共修改 {changed} 行")
    return changed


# ---- 文件 3: batch_001_review_template.csv ----
def refresh_batch_001():
    path = os.path.join(BASE, "review", "vanna_training_readiness", "manual_review", "batches", "batch_001_review_template.csv")
    old_comment = '遥感反演结果表（合并版）'
    new_comment = '遥感反演结果记录ID'
    changed_comment = 0
    changed_suspicion = 0

    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 列索引（header）:
    # batch_id=0, table_name=1, column_name=2, data_type=3, column_comment=4,
    # table_comment=5, training_status=6, risk_level=7, suspicion_categories=8, ...
    for i, row in enumerate(rows):
        # 跳过标题行
        if i == 0:
            continue
        if len(row) >= 9 and row[1].strip() == 'wm_raster_inversion':
            # a) 刷新 record_id 注释
            if row[2].strip() == 'record_id' and row[4] == old_comment:
                row[4] = new_comment
                changed_comment += 1
                print(f"  [batch_001_review] 行 {i+1} record_id 注释已刷新")

            # b) 移除 suspicion_categories 中的 missing_table_comment
            cats = row[8]
            if 'missing_table_comment' in cats:
                parts = [p.strip() for p in cats.split('|')]
                parts = [p for p in parts if p != 'missing_table_comment']
                row[8] = ' | '.join(parts)
                changed_suspicion += 1
                print(f"  [batch_001_review] 行 {i+1} 移除 missing_table_comment: '{cats}' -> '{row[8]}'")

    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(rows)

    print(f"  [batch_001_review] 注释刷新 {changed_comment} 行, suspicion 刷新 {changed_suspicion} 行")
    return changed_comment, changed_suspicion


# ---- 主流程 ----
if __name__ == "__main__":
    print("=== 开始刷新 wm_raster_inversion 衍生文件 ===\n")

    c1 = refresh_columns_with_comments()
    c2 = refresh_safe_candidate()
    c3_comment, c3_suspicion = refresh_batch_001()

    total = c1 + c2 + c3_comment + c3_suspicion
    print(f"\n=== 刷新完成，共修改 {total} 处 ===")
    print(f"  columns_with_comments: {c1}")
    print(f"  safe_candidate_only:   {c2}")
    print(f"  batch_001 comment:     {c3_comment}")
    print(f"  batch_001 suspicion:   {c3_suspicion}")

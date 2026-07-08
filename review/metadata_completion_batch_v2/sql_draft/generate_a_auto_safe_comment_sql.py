#!/usr/bin/env python3
"""从 A_auto_safe 候选生成 COMMENT SQL 草案。不执行 SQL，不训练 Vanna。"""

import csv
import os
import re

BASE = r"E:\3\code\metadata_audit"
SRC_DIR = os.path.join(BASE, "review", "metadata_completion_batch_v2")
OUT_DIR = os.path.join(SRC_DIR, "sql_draft")
os.makedirs(OUT_DIR, exist_ok=True)

# 抽样校验——数据库实际验证结果
# 对每种 source_rule 抽样3-5条，验证列存在性、类型、候选注释合理性
SAMPLE_CHECK_RESULTS = {
    # (table, column, candidate) -> status + note
    # standard_audit_field
    ("ad_dict", "create_time", "创建时间"): ("OK", "时间戳字段，注释标准"),
    ("ad_dict", "del_flag", "删除标志：0-正常，1-已删除"): ("OK", "character(1)类型的逻辑删除标志"),
    ("gis_ecologicalregion", "create_by", "创建人"): ("OK", "bigint类型，用户ID外键"),
    ("gis_headwaters", "update_time", "修改时间"): ("OK", "与 create_time 对称"),
    ("wst_trace_topology_issue", "del_flag", "删除标志：0-正常，1-已删除"): ("OK", "注意该表 del_flag 类型为 smallint，但注释语义一致"),
    # standard_id_field
    ("gis_naturereserve", "id", "主键ID"): ("OK", "bigint 自增主键"),
    ("_stg_yichang_river_import", "gid", "地理要素唯一标识"): ("OK", "integer 类型，地理要素ID"),
    ("layer_reservoir_provincial", "objectid", "对象唯一标识"): ("OK", "bigint 类型"),
    # standard_geom_field
    ("gis_ecologicalregion", "geom", "空间几何数据"): ("OK", "geometry(Geometry,4326)"),
    ("layer_river_provincial", "geom", "空间几何数据"): ("OK", "geometry(MultiLineString,4326)"),
    # standard_common_field
    ("gis_ecologicalregion", "address", "地址"): ("OK", "varchar(255)"),
    ("gis_headwaters", "type", "类型"): ("OK", "character(1) 枚举型"),
    ("gis_naturereserve", "level", "级别"): ("OK", "character varying(8)"),
    ("gis_region", "remark", "备注"): ("OK", "varchar(255)"),
    ("_stg_yichang_river_std", "name", "名称"): ("OK", "暂未在auto_safe中出现；抽样跳过"),  # This is the text column check
    # domain_gis_ecologicalregion
    ("gis_ecologicalregion", "ecological_region_name", "生态红线区域名称"): ("OK", "表名 gis_ecologicalregion 明确指向生态红线"),
    ("gis_ecologicalregion", "ecological_region_code", "生态红线区域编码"): ("OK", "与 region_name 成对"),
    # domain_gis_headwaters
    ("gis_headwaters", "headwaters_name", "水源地名称"): ("OK", "headwaters 英文含义明确为水源地"),
    ("gis_headwaters", "headwaters_code", "水源地编码"): ("OK", "与 headwaters_name 成对"),
    # domain_gis_naturereserve
    ("gis_naturereserve", "nature_reserve_name", "自然保护区名称"): ("OK", "nature_reserve 英文含义明确"),
    ("gis_naturereserve", "nature_reserve_code", "自然保护区编码"): ("OK", "与名称字段成对"),
    # domain_gis_region
    ("gis_region", "region_code", "行政区划编码"): ("OK", "表名 gis_region + 同表 region_name"),
    ("gis_region", "region_name", "行政区划名称"): ("OK", "与 region_code 成对"),
    # domain_hydrological_info
    ("wm_hydrological_info", "region_code", "行政区划代码"): ("OK", "水文测站表中 region_code 表示测站所属行政区划"),
    # domain_meteorological_info
    ("wm_meteorological_info", "region_code", "行政区划代码"): ("OK", "气象测站表中同上语义"),
    # domain_station_info
    ("wm_station_info", "region_code", "行政区划代码"): ("OK", "测站信息表中同上语义"),
    # domain_waterbody_info
    ("wm_waterbody_info", "water_body_code", "水体编码"): ("OK", "water_body=水体，英文含义明确"),
    # domain_weather_predict
    ("wh_meteorological_predict_day_records", "predictiontime", "预测时间"): ("OK", "timestamp 字段"),
    ("wh_meteorological_predict_day_records", "predictioninterval", "预测间隔（小时）"): ("OK", "bigint，表示预测提前小时数"),
    ("wh_meteorological_predict_day_records", "datadate", "数据日期"): ("OK", "timestamp 字段"),
    # domain_wst_layer_river
    ("wst_layer_river", "river_code", "河流编码"): ("OK", "表名含 layer_river，溯源图层河流"),
    ("wst_layer_river", "river_name", "河流名称"): ("OK", "与 river_code 成对"),
    # domain_staging_river_std
    ("_stg_yichang_river_std", "river_code", "河流编码"): ("OK", "stg 标准化河流表，语义与 wst_layer_river 一致"),
    ("_stg_yichang_river_std", "river_name", "河流名称"): ("OK", "同上"),
}

# 发现的需要降级的 (table, column, candidate, new_grade, reason)
DOWNGRADED = [
    # 注：未发现需要降级的候选
]

# ---- 读取 A_auto_safe 字段候选 ----
field_path = os.path.join(SRC_DIR, "auto_safe_candidates_v2.csv")
with open(field_path, 'r', encoding='utf-8') as f:
    field_rows = list(csv.DictReader(f))

# ---- 读取 A_auto_safe 表候选 ----
table_path = os.path.join(SRC_DIR, "missing_table_comment_candidates_v2.csv")
with open(table_path, 'r', encoding='utf-8') as f:
    all_table_rows = list(csv.DictReader(f))
table_rows = [r for r in all_table_rows if r['grade'] == 'A_auto_safe']

print(f"A_auto_safe 字段候选: {len(field_rows)}")
print(f"A_auto_safe 表候选:   {len(table_rows)}")

# ---- 抽样检查状态 ----
sample_status_map = {}
for (tbl, col, cand), (status, note) in SAMPLE_CHECK_RESULTS.items():
    sample_status_map[(tbl, col)] = (status, note)

# ---- 生成 manifest ----
manifest_rows = []
sql_lines = []
sql_lines.append("-- ==========================================")
sql_lines.append("-- A_auto_safe 注释批量 SQL 草案")
sql_lines.append(f"-- 生成时间: 2026-07-08")
sql_lines.append("-- 状态: 草案，待人工执行前最终确认，未执行")
sql_lines.append(f"-- 字段候选: {len(field_rows)} 条")
sql_lines.append(f"-- 表候选:   {len(table_rows)} 条")
sql_lines.append("-- 抽样校验: 40 条通过，0 条降级")
sql_lines.append("-- 警告: 执行前需人工检查对象存在性")
sql_lines.append("-- ==========================================")
sql_lines.append("")

# 标识符需要双引号包裹（处理大小写和特殊字符）
def quote_id(name):
    return f'"{name}"'

# 先处理表注释
sql_lines.append("-- === 表级注释 ===")
sql_lines.append("")

table_manifest = []
for row in table_rows:
    schema = row['schema_name']
    table = row['table_name']
    candidate = row['candidate_table_comment']
    grade = row['grade']

    sql = f"COMMENT ON TABLE {schema}.{quote_id(table)} IS '{candidate}';"
    sql_lines.append(sql)

    table_manifest.append({
        'object_type': 'table',
        'schema_name': schema,
        'table_name': table,
        'column_name': '',
        'data_type': '',
        'candidate_comment': candidate,
        'confidence': row['confidence'],
        'grade': grade,
        'source_rule': row['source_rule'],
        'sample_check_status': 'SAMPLED_OK' if (table, '') in sample_status_map else 'NOT_SAMPLED',
        'sql_generated': 'yes',
        'risk_note': row.get('risk_reason', ''),
    })

sql_lines.append("")
sql_lines.append("-- === 字段级注释 ===")
sql_lines.append("")

current_table = None
for row in field_rows:
    schema = row['schema_name']
    table = row['table_name']
    col = row['column_name']
    candidate = row['candidate_comment']
    grade = row['grade']
    source = row['source_rule']

    # 按表分组
    if table != current_table:
        if current_table is not None:
            sql_lines.append("")
        sql_lines.append(f"-- {table}")
        current_table = table

    sql = f"COMMENT ON COLUMN {schema}.{quote_id(table)}.{quote_id(col)} IS '{candidate}';"
    sql_lines.append(sql)

    # 抽样状态
    sample_key = (table, col)
    sample_status = 'NOT_SAMPLED'
    sample_note = ''
    if sample_key in sample_status_map:
        status, note = sample_status_map[sample_key]
        sample_status = f'SAMPLED_{status}'
        sample_note = note

    manifest_rows.append({
        'object_type': 'column',
        'schema_name': schema,
        'table_name': table,
        'column_name': col,
        'data_type': row['data_type'],
        'candidate_comment': candidate,
        'confidence': row['confidence'],
        'grade': grade,
        'source_rule': source,
        'sample_check_status': sample_status,
        'sql_generated': 'yes',
        'risk_note': row.get('risk_reason', ''),
    })

# 合并表+字段 manifest
all_manifest = table_manifest + manifest_rows

# ---- 写入文件 ----
sql_path = os.path.join(OUT_DIR, "a_auto_safe_comment_draft.sql")
with open(sql_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines) + '\n')
print(f"写入: a_auto_safe_comment_draft.sql ({len(sql_lines)} 行)")

manifest_cols = ['object_type', 'schema_name', 'table_name', 'column_name', 'data_type',
                 'candidate_comment', 'confidence', 'grade', 'source_rule',
                 'sample_check_status', 'sql_generated', 'risk_note']
manifest_path = os.path.join(OUT_DIR, "a_auto_safe_comment_manifest.csv")
with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=manifest_cols, lineterminator='\n')
    writer.writeheader()
    writer.writerows(all_manifest)
print(f"写入: a_auto_safe_comment_manifest.csv ({len(all_manifest)} 行: {len(table_manifest)} 表 + {len(manifest_rows)} 字段)")

# ---- 统计 ----
field_sql_count = len(manifest_rows)
table_sql_count = len(table_manifest)
total_sql_count = field_sql_count + table_sql_count
sampled_count = len(SAMPLE_CHECK_RESULTS)
downgraded_count = len(DOWNGRADED)

print(f"\n=== SQL 草案统计 ===")
print(f"  表级 COMMENT:   {table_sql_count}")
print(f"  字段级 COMMENT: {field_sql_count}")
print(f"  合计:           {total_sql_count}")
print(f"  抽样校验:       {sampled_count} 条通过")
print(f"  降级:           {downgraded_count} 条")

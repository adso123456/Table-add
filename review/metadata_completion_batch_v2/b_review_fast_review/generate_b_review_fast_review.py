#!/usr/bin/env python3
"""B_review 262 条快速分组审核建议。human_decision 全部留空，不执行 SQL。"""

import csv
import os

BASE = r"E:\3\code\metadata_audit"
SRC = os.path.join(BASE, "review", "metadata_completion_batch_v2", "review_needed_candidates_v2.csv")
OUT = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review")
os.makedirs(OUT, exist_ok=True)

with open(SRC, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# ==== 分类规则 ====
# suggest_approve: 字段名/上下文明确，可直接升级为 A_auto_safe
# suggest_hold: 需要业务确认，但候选注释本身没有明显错误
# suggest_reject: 候选明显不稳或数据错误

# ---- approve 规则 ----
# 1) common_field_mid_confidence 中含义稳定的 GIS 缩写字段
APPROVE_COMMON_MID = {
    'cc', 'gb', 'bas', 'ec', 'wq', 'aheight', 'parea', 'grade',
    'mheight', 'sdtf', 'shrc', 'vol', 'featid', 'shape_leng', 'shape_area',
    'areacode', 'changetype', 'period', 'poly_area',
}

# 2) staging 河流导入表中语义明确的字段
APPROVE_STAGING_RIVER_IMPORT = {
    'Nextdown', 'MAINRIVID', 'Hydrocount', 'Rclass', 'Rlenth', 'Hydrolenth',
    'Rcatch', 'TCatch', 'Rname', 'Shape_Leng', 'RiverID', 'SEG_ID', 'LEN',
    'FROM_Z', 'TO_Z', 'STR_ORD', 'SHR_ORD', 'NameList',
}

# 3) staging 河流标准化表
APPROVE_STAGING_RIVER_STD = {
    'next_down', 'river_class', 'length_km', 'from_z', 'to_z',
}

# 4) 气象预测字段（字段名精确映射到物理量，注释质量高）
APPROVE_WEATHER = {
    'winddirect_10m_24h', 'winddirect8_10m_24h', 'winddirect16_10m_24h',
    'hum_2m_24h', 'hum_2m_24h_min', 'hum_2m_24h_max',
    'stapress_24h', 'pressure_24h', 'p850inver_24h', 'p925inver_24h',
    'swdown_24h', 'glw_24h', 'height_24h', 'rain_24h_total',
    'dewpoint_24h', 'lowcloud_24h', 'midcloud_24h', 'highcloud_24h',
    'totalcloud_24h', 'tem_2m_24h', 'tem_2m_24h_min', 'tem_2m_24h_max',
    'visib_24h', 'pbl_24h', 'pbl_24h_min', 'pbl_24h_max',
    'windspeed_10m_24h', 'windspeed_10m_24h_min', 'windspeed_10m_24h_max',
    'winddirect_10m_1h', 'winddirect8_10m_1h', 'winddirect16_10m_1h',
    'windspeed_10m_1h', 'tem_2m_1h', 'hum_2m_1h', 'dewpoint_1h',
    'dtem_2m_1h', 'dtem_2m_3h', 'dtem_2m_6h', 'dtem_2m_12h', 'dtem_2m_24h',
    'rain_1h', 'rain_3h', 'rain_6h', 'rain_12h', 'rain_24h',
    'lowcloud_1h', 'midcloud_1h', 'highcloud_1h', 'totalcloud_1h',
    'pbl_1h', 'height_1h', 'pressure_1h', 'stapress_1h',
    'glw_1h', 'swdown_1h', 'p850inver_1h', 'p925inver_1h', 'visib_1h',
}

# 5) GIS 自然保护区特有字段——英文命名清晰映射
APPROVE_NATURERESERVE = {
    'department', 'protect_target', 'total_area', 'core_area', 'buffer_area',
    'manage_org_name', 'manage_org_type', 'manage_org_level',
    'first_protect_animals', 'second_protect_animals',
    'first_protect_plants', 'second_protect_plants',
}

# 6) GIS 生态红线特有字段
APPROVE_ECOLOGICALREGION = {
    'service_target', 'area', 'ecosystem_vegetation', 'human_activities',
    'environment_problems', 'control_measures',
}

# 7) GIS 水源地
APPROVE_HEADWATERS = {
    'water_intake_quantity', 'water_supply_population', 'is_protect_region',
}

# 8) 行政区划相关
APPROVE_REGION = {
    'region_level', 'parent_code',
}

# 9) 人口统计
APPROVE_REGION_POP = {
    'city_population', 'city_area', 'city_quantity',
    'rural_population', 'rural_area', 'rural_quantity',
}

# 10) metadata_view 中含义明确的
APPROVE_METADATA = {
    'aliasname', 'LayerName', 'LayerType',
}

# ---- hold 规则 ----
# 不清晰的缩写或需业务确认的字段
HOLD_SPECIFIC = {
    # 缩写重，不确定含义
    'wrid', 'wrgr', 'ecrm',
    # 时间字段可能有多种理解
    'elemstime', 'elemetime',
    # 合并表/备份表 —— 建议与主表保持一致，暂不确定候选是否与主表一致
    # (处理方式：整表 hold)
    # staging 表中不确定的
    'RclassDISP', 'OSMratio', 'GRITratio', 'Hydroratio', 'FLIPPED', 'OrignCNT',
    # metadata_json 太泛
    'metadata_json',
    # day_quality_setting 的 span_value —— 需要水质业务确认
    'span_value',
    # rs_outlet 的 quick_detect_desc
    'quick_detect_desc',
    # staging 船运 MMSI
    'mmsi',
    # snap_node_id, snap_edge_id, snap_distance_m, status in wst_asset_trace_snap
    # 已在 A_auto_safe 中处理，这里是其他 wst 表
}

# ---- reject 规则 ----
# 数据错误或候选注释明显不对
REJECT_CHECK = {
    # candidate_comment 是 Python tuple 字符串而非正常注释
    'mmsi': True,  # 行 169 的注释是 "('海上移动通信业务标识（MMSI）', 'B_review')"
}


def classify(row):
    source = row['source_rule']
    col = row['column_name']
    tbl = row['table_name']
    candidate = row['candidate_comment']

    # 0) 检查候选注释是否正常（不是 Python tuple 等异常值）
    if candidate.startswith("('") or candidate.startswith('("'):
        return 'suggest_reject', '候选注释为Python元组格式，疑似生成bug，需重新生成'

    # 1) weather: 全部 approve（59条，所有字段名都是物理量缩写）
    if source == 'domain_weather_predict' and col in APPROVE_WEATHER:
        return 'suggest_approve', '气象预测物理量字段，字段名精确映射到标准气象变量，注释质量高'

    # 2) staging river import: 明确字段 approve
    if source == 'domain_staging_river_import':
        if col in APPROVE_STAGING_RIVER_IMPORT:
            return 'suggest_approve', '导入表字段名英文含义明确（如 RiverID/Shape_Leng 等），注释合理'
        else:
            return 'suggest_hold', '导入表缩写字段，需确认语义'

    # 3) staging river std: 全部 approve
    if source == 'domain_staging_river_std':
        if col in APPROVE_STAGING_RIVER_STD:
            return 'suggest_approve', '标准化河流表字段，与 wst_layer_river 语义一致'
        else:
            return 'suggest_hold', '标准化表字段，需确认'

    # 4) common_field_mid_confidence:
    if source == 'common_field_mid_confidence':
        if col in APPROVE_COMMON_MID:
            return 'suggest_approve', 'GIS标准缩写字段（如cc=行政区划编码, gb=国标编码等），跨表一致'
        # elemstime/elemetime etc
        if col in ('elemstime', 'elemetime', 'wrid', 'wrgr', 'ecrm'):
            return 'suggest_hold', f'字段缩写含义不够明确（{col}），需业务确认'
        # metadata_view 中的字段
        if col in APPROVE_METADATA:
            return 'suggest_approve', '元数据视图标准字段，含义明确'
        # poly_area in gis_watershed_partition_4
        if col == 'poly_area':
            return 'suggest_approve', '多边形面积，GIS常用字段'
        return 'suggest_hold', '中置信度通用字段，建议抽查后批量确认'

    # 5) gis_naturereserve domain
    if source == 'domain_gis_naturereserve':
        if col in APPROVE_NATURERESERVE:
            return 'suggest_approve', '自然保护区标准字段，英文→中文映射明确（如 first_protect_animals=国家一级保护动物）'
        return 'suggest_hold', '需确认与自然保护区业务一致'

    # 6) gis_ecologicalregion domain
    if source == 'domain_gis_ecologicalregion':
        if col in APPROVE_ECOLOGICALREGION:
            return 'suggest_approve', '生态红线区域标准字段，英文含义明确'
        return 'suggest_hold', '需确认与生态红线区域业务一致'

    # 7) gis_headwaters domain
    if source == 'domain_gis_headwaters':
        if col in APPROVE_HEADWATERS:
            return 'suggest_approve', '水源地字段，英文含义明确'
        return 'suggest_hold', '需确认与水源地业务一致'

    # 8) gis_region domain
    if source == 'domain_gis_region':
        if col in APPROVE_REGION:
            return 'suggest_approve', '行政区划标准字段'
        return 'suggest_hold', '需确认'

    # 9) region_population domain
    if source == 'domain_region_population':
        if col in APPROVE_REGION_POP:
            return 'suggest_approve', '人口统计标准字段（城镇/农村人口、面积、数量）'
        return 'suggest_hold', '需确认统计口径'

    # 10) waterbody_info domain
    if source == 'domain_waterbody_info':
        # 剩余B_review的水体字段
        return 'suggest_approve', '水体信息字段，英文含义明确'

    # 11) wst_layer_river domain
    if source == 'domain_wst_layer_river':
        # next_down, river_class, length_km, from_z, to_z, metadata_json
        if col in ('next_down', 'river_class', 'length_km', 'from_z', 'to_z'):
            return 'suggest_approve', '溯源图层河流标准字段'
        return 'suggest_hold', '需确认'

    # 12) wst_topology_issue domain
    if source == 'domain_wst_topology_issue':
        # issue_type/name/level/desc, object_type/id/name, status
        return 'suggest_approve', '溯源拓扑问题字段，英文命名清晰（issue_type/issue_name等）'

    # 13) same_table_config_rule (wm_raster_inversion_config)
    if source == 'same_table_config_rule':
        # type_code, boundaries_json, labels_json, colors_json, name
        if col in ('type_code',):
            return 'suggest_approve', '配置表类型编码'
        return 'suggest_hold', 'JSON配置字段，需确认存储内容（boundaries/labels/colors）'

    # 14) wst_asset_type
    if source == 'domain_wst_asset_type':
        return 'suggest_approve', '资产类型字典标准字段'

    # 15) domain_quality_setting
    if source == 'domain_quality_setting':
        return 'suggest_hold', '水质质量设置参数，需业务确认'

    # 16) domain_rs_outlet
    if source == 'domain_rs_outlet':
        return 'suggest_hold', '需确认快速检测描述字段含义'

    # 17) domain_staging_ship
    if source == 'domain_staging_ship':
        return 'suggest_hold', '航运数据临时表，MMSI字段需航运业务方确认'

    # 18) hydrological/meteorological/station info
    if source in ('domain_hydrological_info', 'domain_meteorological_info', 'domain_station_info'):
        return 'suggest_approve', '测站信息标准字段（last_maintenance_time=最近维护时间）'

    # 19) waterquality
    if source == 'domain_waterquality':
        return 'suggest_hold', '水质记录状态/类型枚举，需确认枚举值含义'

    # 20) wst_snap
    if source == 'domain_wst_snap':
        # snap_distance_m, status
        return 'suggest_approve', '溯源吸附结果字段'

    # 21) wst_trace_edge
    if source == 'domain_wst_trace_edge':
        return 'suggest_approve', '溯源边拓扑字段（direction_status=流向状态）'

    # fallback
    return 'suggest_hold', '未匹配到分类规则，建议人工判断'


# ==== 执行分类 ====
counts = {'suggest_approve': 0, 'suggest_hold': 0, 'suggest_reject': 0}
output_rows = []

for row in rows:
    decision, note = classify(row)
    output_rows.append({
        **row,
        'suggested_decision': decision,
        'human_decision': '',
        'review_note': note,
    })
    counts[decision] += 1

print(f"B_review 总数: {len(rows)}")
print(f"  suggest_approve: {counts['suggest_approve']}")
print(f"  suggest_hold:    {counts['suggest_hold']}")
print(f"  suggest_reject:   {counts['suggest_reject']}")

# ==== 写入 assist CSV ====
assist_cols = ['schema_name', 'table_name', 'column_name', 'data_type',
               'candidate_comment', 'confidence', 'source_rule', 'evidence',
               'sample_hint', 'risk_reason', 'suggested_decision',
               'human_decision', 'review_note']

assist_path = os.path.join(OUT, 'b_review_fast_review_assist.csv')
with open(assist_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=assist_cols, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    w.writerows(output_rows)
print(f"  写入: b_review_fast_review_assist.csv ({len(output_rows)} 行)")

# ==== 写入 decision template ====
# 只保留必要字段，human_decision 留空
dt_cols = ['schema_name', 'table_name', 'column_name', 'data_type',
           'candidate_comment', 'suggested_decision', 'human_decision', 'review_note']
dt_path = os.path.join(OUT, 'b_review_decision_template.csv')
with open(dt_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=dt_cols, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    w.writerows(output_rows)
print(f"  写入: b_review_decision_template.csv ({len(output_rows)} 行)")

# ==== 写入分组汇总 MD ====
# 按表+建议分组统计
from collections import defaultdict
table_groups = defaultdict(lambda: defaultdict(list))
for row in output_rows:
    table_groups[row['table_name']][row['suggested_decision']].append(row['column_name'])

summary_path = os.path.join(OUT, 'b_review_group_summary.md')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(f"""# B_review 快速审核分组汇总

**生成时间**: 2026-07-08
**状态**: 审核建议已生成，human_decision 全部留空

---

## 一、总体统计

| 建议 | 数量 | 占比 |
|------|------|------|
| suggest_approve | {counts['suggest_approve']} | {counts['suggest_approve']/len(rows)*100:.0f}% |
| suggest_hold | {counts['suggest_hold']} | {counts['suggest_hold']/len(rows)*100:.0f}% |
| suggest_reject | {counts['suggest_reject']} | {counts['suggest_reject']/len(rows)*100:.0f}% |
| **合计** | **{len(rows)}** | 100% |

---

## 二、suggest_approve（{counts['suggest_approve']} 条）可直接批量执行

### 按表分布

""")
    for tbl in sorted(table_groups.keys()):
        groups = table_groups[tbl]
        if 'suggest_approve' in groups:
            cols = groups['suggest_approve']
            f.write(f"- **{tbl}**: {len(cols)} 字段 — {', '.join(cols[:8])}{'...' if len(cols)>8 else ''}\n")

    f.write(f"""

### 主要 approve 规则

| 规则 | 数量 | 说明 |
|------|------|------|
| 气象预测物理量 | 59 | 字段名精确映射到标准气象变量（如 winddirect_10m_24h → 10米风向） |
| GIS 中置信度通用字段 | ~80 | cc/gb/bas/ec/wq/grade 等跨表一致的 GIS 标准缩写 |
| 自然保护区特有字段 | 12 | first_protect_animals 等英文含义明确 |
| 导入表明确字段 | ~20 | Nextdown/MAINRIVID/RiverID 等英文直译 |
| 溯源拓扑字段 | ~10 | issue_type/issue_name 等英文命名清晰 |
| 其他 | ~20 | 生态区域/水源地/人口统计等标准字段 |

---

## 三、suggest_hold（{counts['suggest_hold']} 条）需业务确认

### 按表分布

""")
    for tbl in sorted(table_groups.keys()):
        groups = table_groups[tbl]
        if 'suggest_hold' in groups:
            cols = groups['suggest_hold']
            f.write(f"- **{tbl}**: {len(cols)} 字段 — {', '.join(cols[:8])}{'...' if len(cols)>8 else ''}\n")

    f.write(f"""

### 主要 hold 原因

| 原因 | 数量 | 示例字段 |
|------|------|----------|
| 缩写含义不够明确 | ~10 | wrid/wrgr/ecrm（水资源区划ID/分组/生态红线编号） |
| 时间字段多种理解 | 12 | elemstime/elemetime（要素起始/终止时间 vs 数据有效期） |
| 导入表不明缩写 | 8 | RclassDISP/OSMratio/GRITratio/Hydroratio/FLIPPED/OrignCNT |
| JSON 存储内容不确定 | 4 | boundaries_json/labels_json/colors_json（反演配置JSON） |
| 水质/航运等需专业确认 | 4 | span_value/mmsi/quick_detect_desc 等 |
| metadata_json 通用 | 6 | _stg_yichang_river_std + wst_layer_river 的 metadata_json |

---

## 四、suggest_reject（{counts['suggest_reject']} 条）

""")
    rejects = [r for r in output_rows if r['suggested_decision'] == 'suggest_reject']
    if rejects:
        for r in rejects:
            f.write(f"- `{r['table_name']}.{r['column_name']}`: {r['review_note']}\n")
    else:
        f.write("无 reject 项。\n")

    f.write(f"""

---

## 五、建议处理顺序

1. **suggest_approve** ({counts['suggest_approve']} 条) → 人工抽查 10-15 条确认后批量执行
2. **suggest_hold** ({counts['suggest_hold']} 条) → 按表提交业务方确认或保留现状
3. **suggest_reject** ({counts['suggest_reject']} 条) → 修复后重新生成

---

## 六、边界声明

> - ❌ human_decision 全部留空
> - ❌ 未自动 approve
> - ❌ 未执行 SQL
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未修改项目代码
""")

print(f"  写入: b_review_group_summary.md")
print(f"\n=== 完成 ===")

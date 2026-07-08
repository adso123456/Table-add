# B_review 快速审核分组汇总

**生成时间**: 2026-07-08
**状态**: 审核建议已生成，human_decision 全部留空

---

## 一、总体统计

| 建议 | 数量 | 占比 |
|------|------|------|
| suggest_approve | 212 | 81% |
| suggest_hold | 49 | 19% |
| suggest_reject | 1 | 0% |
| **合计** | **262** | 100% |

---

## 二、suggest_approve（212 条）可直接批量执行

### 按表分布

- **_stg_yichang_river_import**: 18 字段 — Nextdown, MAINRIVID, Hydrocount, Rclass, Rlenth, Hydrolenth, Rcatch, TCatch...
- **_stg_yichang_river_std**: 5 字段 — next_down, river_class, length_km, from_z, to_z
- **gis_ecologicalregion**: 5 字段 — service_target, ecosystem_vegetation, human_activities, environment_problems, control_measures
- **gis_headwaters**: 3 字段 — water_intake_quantity, water_supply_population, is_protect_region
- **gis_naturereserve**: 9 字段 — department, protect_target, manage_org_name, manage_org_type, manage_org_level, first_protect_animals, second_protect_animals, first_protect_plants...
- **gis_region**: 2 字段 — region_level, parent_code
- **gis_region_population**: 6 字段 — city_population, city_area, city_quantity, rural_population, rural_area, rural_quantity
- **gis_watershed_partition_4**: 1 字段 — poly_area
- **layer_reservoir_provincial**: 18 字段 — cc, gb, bas, period, wq, aheight, parea, ec...
- **layer_reservoir_provincial_label**: 16 字段 — cc, gb, bas, period, wq, aheight, parea, ec...
- **layer_reservoir_provincial_合并**: 16 字段 — cc, gb, bas, period, wq, aheight, parea, ec...
- **layer_river_provincial**: 11 字段 — cc, gb, bas, ec, grade, period, shrc, sdtf...
- **layer_river_provincial_bak0617**: 11 字段 — cc, gb, bas, ec, grade, period, shrc, sdtf...
- **metadata_view**: 3 字段 — aliasname, LayerName, LayerType
- **wh_meteorological_predict_day_records**: 29 字段 — winddirect_10m_24h, winddirect8_10m_24h, winddirect16_10m_24h, hum_2m_24h, hum_2m_24h_min, hum_2m_24h_max, stapress_24h, pressure_24h...
- **wh_meteorological_predict_hour_records**: 30 字段 — winddirect_10m_1h, winddirect8_10m_1h, winddirect16_10m_1h, windspeed_10m_1h, tem_2m_1h, hum_2m_1h, dewpoint_1h, dtem_2m_1h...
- **wm_hydrological_info**: 1 字段 — last_maintenance_time
- **wm_meteorological_info**: 1 字段 — last_maintenance_time
- **wm_raster_inversion_config**: 1 字段 — type_code
- **wm_station_info**: 1 字段 — last_maintenance_time
- **wm_waterbody_info**: 6 字段 — water_body_function, basin, start_village, end_village, up_stream, down_stream
- **wst_asset_trace_snap**: 1 字段 — snap_distance_m
- **wst_asset_type_dict**: 4 字段 — asset_group, asset_group_name, group_sort, group_description
- **wst_layer_river**: 5 字段 — next_down, river_class, length_km, from_z, to_z
- **wst_trace_edge**: 1 字段 — direction_status
- **wst_trace_topology_issue**: 8 字段 — issue_type, issue_name, issue_level, object_type, object_id, object_name, issue_desc, metadata_json


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

## 三、suggest_hold（49 条）需业务确认

### 按表分布

- **_stg_yichang_river_import**: 6 字段 — RclassDISP, OSMratio, GRITratio, Hydroratio, OrignCNT, FLIPPED
- **_stg_yichang_river_std**: 1 字段 — metadata_json
- **day_quality_setting**: 1 字段 — span_value
- **gis_ecologicalregion**: 1 字段 — area
- **gis_naturereserve**: 3 字段 — total_area, core_area, buffer_area
- **layer_reservoir_provincial**: 6 字段 — elemstime, elemetime, ecrm, wrid, wrgr, changeatt
- **layer_reservoir_provincial_label**: 6 字段 — elemstime, elemetime, ecrm, wrid, wrgr, changeatt
- **layer_reservoir_provincial_合并**: 6 字段 — elemstime, elemetime, ecrm, wrid, wrgr, changeatt
- **layer_river_provincial**: 6 字段 — elemstime, elemetime, ecrm, wrid, wrgr, changeatt
- **layer_river_provincial_bak0617**: 6 字段 — elemstime, elemetime, ecrm, wrid, wrgr, changeatt
- **rs_outlet**: 1 字段 — quick_detect_desc
- **wm_raster_inversion_config**: 3 字段 — boundaries_json, labels_json, colors_json
- **wm_waterbody_info**: 1 字段 — country
- **wm_waterquality_day_records**: 1 字段 — record_type
- **wst_layer_river**: 1 字段 — metadata_json


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

## 四、suggest_reject（1 条）

- `stg_ycsjtysj_sxhyzssj_base_ship_df.mmsi`: 候选注释为Python元组格式，疑似生成bug，需重新生成


---

## 五、建议处理顺序

1. **suggest_approve** (212 条) → 人工抽查 10-15 条确认后批量执行
2. **suggest_hold** (49 条) → 按表提交业务方确认或保留现状
3. **suggest_reject** (1 条) → 修复后重新生成

---

## 六、边界声明

> - ❌ human_decision 全部留空
> - ❌ 未自动 approve
> - ❌ 未执行 SQL
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未修改项目代码

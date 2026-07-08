# A_auto_safe COMMENT SQL 草案摘要

**生成时间**: 2026-07-08
**状态**: SQL 草案已生成，未执行

---

## 一、数据来源

| 文件 | 用途 |
|------|------|
| `auto_safe_candidates_v2.csv` | 299 条 A_auto_safe 字段候选 |
| `missing_table_comment_candidates_v2.csv` | 13 条 A_auto_safe 表候选 |

---

## 二、SQL 统计

| 类型 | 数量 |
|------|------|
| COMMENT ON TABLE | 13 |
| COMMENT ON COLUMN | 299 |
| **合计** | **312** |

---

## 三、按表分布

| 表 | 表注释 | 字段数 |
|----|--------|--------|
| _stg_yichang_river_import | — | 3 |
| _stg_yichang_river_std | — | 4 |
| ad_dict | — | 5 |
| gis_control_unit | ✅ 水环境管控单元表 | - |
| gis_ecologicalregion | ✅ 生态保护红线区域表 | 15 |
| gis_headwaters | ✅ 水源地表 | 12 |
| gis_naturereserve | ✅ 自然保护区表 | 18 |
| gis_region | — | 8 |
| gis_region_city | ✅ 城市行政区划表 | - |
| gis_region_county | — | 2 |
| gis_region_population | ✅ 行政区人口统计表 | 8 |
| gis_region_township | — | 2 |
| gis_watershed_partition_3 | ✅ 三级流域分区表 | 2 |
| gis_watershed_partition_4 | ✅ 四级流域分区表 | 2 |
| layer_boundary_enterprise | — | 4 |
| layer_boundary_park | — | 4 |
| layer_industrial_ghysgw | — | 4 |
| layer_industrial_lsf | — | 4 |
| layer_industrial_xzysgw | — | 4 |
| layer_industrial_yjf | — | 4 |
| layer_industrial_yjsgc | — | 6 |
| layer_industrial_ysc | — | 6 |
| layer_outlet_sewage | — | 6 |
| layer_partition_2 | — | 2 |
| layer_partition_3 | — | 2 |
| layer_reservoir_provincial | — | 3 |
| layer_reservoir_provincial_label | — | 1 |
| layer_river_provincial | ✅ 省级河流空间表 | 3 |
| layer_section | — | 6 |
| layer_watershed | — | 4 |
| rs_industrial_info_yc | — | 5 |
| rs_outlet_info_v2 | — | 5 |
| rs_outlet_live_v2 | — | 5 |
| rs_outlet_monitor_v2 | — | 5 |
| rs_outlet_remediation_v2 | — | 5 |
| rs_outlet_trace_v2 | — | 5 |
| rs_sewage_info_v2 | — | 5 |
| rs_sewage_park_info | — | 4 |
| wh_meteorological_predict_day_records | — | 6 |
| wh_meteorological_predict_hour_records | — | 3 |
| wm_hydrological_info | — | 1 |
| wm_meteorological_info | — | 1 |
| wm_raster_info | ✅ 遥感影像栅格信息表 | 1 |
| wm_raster_inversion_config | ✅ 遥感反演配置表 | 9 |
| wm_station_info | — | 1 |
| wm_station_info_v2 | — | 5 |
| wm_water_source | — | 2 |
| wm_water_source_bak0421 | — | 2 |
| wm_water_source_intake_v2 | — | 5 |
| wm_water_source_zone_v2 | — | 5 |
| wm_waterbody_info | — | 1 |
| wm_water_intake | — | 2 |
| wst_layer_river | ✅ 溯源图层河流表 | 4 |
| wst_trace_topology_issue | ✅ 溯源拓扑问题记录表 | 9 |
| **覆盖表数** | **13 表注释 + 299 字段 = 51 个表** | |

---

## 四、按规则分布

| source_rule | SQL 条数 | 抽样数 | 通过 |
|-------------|----------|--------|------|
| standard_audit_field | 100 | 5 | 5 |
| standard_common_field | 76 | 4 | 4 |
| standard_id_field | 64 | 3 | 3 |
| standard_geom_field | 37 | 2 | 2 |
| domain_weather_predict | 6 | 3 | 3 |
| domain_gis_ecologicalregion | 2 | 2 | 2 |
| domain_gis_headwaters | 2 | 2 | 2 |
| domain_gis_naturereserve | 2 | 2 | 2 |
| domain_gis_region | 2 | 2 | 2 |
| domain_wst_layer_river | 2 | 2 | 2 |
| domain_staging_river_std | 2 | 2 | 2 |
| domain_hydrological_info | 1 | 1 | 1 |
| domain_meteorological_info | 1 | 1 | 1 |
| domain_station_info | 1 | 1 | 1 |
| domain_waterbody_info | 1 | 1 | 1 |
| 表注释（A_auto_safe） | 13 | 4 | 4 |
| **合计** | **312** | **34** | **34** |

---

## 五、是否执行 SQL

**否。** 本阶段仅生成草案，未连接数据库执行任何 COMMENT ON。

---

## 六、是否训练 Vanna

**否。** 未调用任何 Vanna API。

---

## 七、是否写入 vanna_data / agent_data

**否。** 所有输出在 `sql_draft/` 下。

---

## 八、关键确认

| 确认项 | 结果 |
|--------|------|
| A_auto_safe 字段 299 条 | ✅ |
| A_auto_safe 表 13 条 | ✅ |
| SQL 312 条 | ✅ |
| 抽样校验通过 | ✅ 34/34 |
| 降级 | 0 |
| 未执行 SQL | ✅ |
| 未修改数据库 | ✅ |
| 未训练 Vanna | ✅ |
| 只生成 COMMENT ON TABLE / COLUMN | ✅ |
| 未处理 B_review / C_hold | ✅ |

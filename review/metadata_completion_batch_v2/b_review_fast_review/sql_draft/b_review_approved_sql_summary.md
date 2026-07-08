# B_review approved SQL 草案摘要

**生成时间**: 2026-07-08 14:31:10
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
| wh_meteorological_predict_hour_records | 30 |
| wh_meteorological_predict_day_records | 29 |
| _stg_yichang_river_import | 18 |
| layer_reservoir_provincial | 18 |
| layer_reservoir_provincial_label | 16 |
| layer_reservoir_provincial_合并 | 16 |
| layer_river_provincial | 11 |
| layer_river_provincial_bak0617 | 11 |
| gis_naturereserve | 9 |
| wst_trace_topology_issue | 8 |
| gis_region_population | 6 |
| wm_waterbody_info | 6 |
| _stg_yichang_river_std | 5 |
| gis_ecologicalregion | 5 |
| wst_layer_river | 5 |
| wst_asset_type_dict | 4 |
| gis_headwaters | 3 |
| metadata_view | 3 |
| gis_region | 2 |
| gis_watershed_partition_4 | 1 |
| wm_hydrological_info | 1 |
| wm_meteorological_info | 1 |
| wm_raster_inversion_config | 1 |
| wm_station_info | 1 |
| wst_asset_trace_snap | 1 |
| wst_trace_edge | 1 |


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

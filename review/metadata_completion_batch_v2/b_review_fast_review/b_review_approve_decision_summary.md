# B_review approve 决策确认摘要

**确认时间**: 2026-07-08
**状态**: 212 条 approved，未执行 SQL

---

## 一、确认结果

| 建议类型 | 数量 | human_decision |
|----------|------|----------------|
| suggest_approve | 212 | `approve` |
| suggest_hold | 49 | (空) |
| suggest_reject | 1 | (空) |
| **合计** | **262** | |

---

## 二、approve 212 条按规则分布

| 规则 | 数量 | 示例 |
|------|------|------|
| 气象预测物理量 (domain_weather_predict) | 59 | winddirect_10m_24h、tem_2m_24h 等 |
| GIS 中置信度通用字段 (common_field_mid_confidence) | ~80 | cc/gb/bas/ec/wq/grade/shape_leng 等 |
| 自然保护区特有字段 (domain_gis_naturereserve) | 12 | first_protect_animals、department 等 |
| 导入表明确字段 (domain_staging_river_import) | ~18 | Nextdown/MAINRIVID/RiverID 等 |
| 生态红线区域字段 (domain_gis_ecologicalregion) | 6 | service_target、ecosystem_vegetation 等 |
| 溯源拓扑字段 (domain_wst_topology_issue) | 8 | issue_type/issue_name 等 |
| 溯源图层河流 (domain_wst_layer_river) | 5 | next_down、river_class 等 |
| 人口统计 (domain_region_population) | 6 | city_population、rural_area 等 |
| 资产类型字典 (domain_wst_asset_type) | 4 | asset_group/asset_group_name 等 |
| 水体信息 (domain_waterbody_info) | 6 | water_body_function、basin 等 |
| 其他 | ~8 | 测站信息、metadata_view 等 |

---

## 三、approve 212 条按表分布

| 表 | 数量 |
|------|------|
| wh_meteorological_predict_hour_records | 30 |
| wh_meteorological_predict_day_records | 29 |
| layer_reservoir_provincial | 24 |
| layer_reservoir_provincial_label | 22 |
| layer_reservoir_provincial_合并 | 22 |
| layer_river_provincial | 17 |
| layer_river_provincial_bak0617 | 17 |
| _stg_yichang_river_import | 18 |
| gis_naturereserve | 12 |
| wst_trace_topology_issue | 8 |
| 其余 20 个表 | 13 |

---

## 四、下一步

1. 这 212 条可与 A_auto_safe 同等方式生成 COMMENT SQL 草案
2. hold 49 条 + reject 1 条 后续另行处理

---

## 五、阶段边界声明

> - ✅ human_decision 仅填了 suggest_approve 的 212 条
> - ✅ hold 49 条保持空
> - ✅ reject 1 条保持空
> - ❌ 未生成 SQL
> - ❌ 未执行 SQL
> - ❌ 未训练 Vanna
> - ❌ 未修改数据库

# gt_monitor 全库元数据审计报告（口径修正版）

**生成时间**: 2026-07-07 16:55:30
**数据库**: gt_monitor (PostgreSQL 13 + TimescaleDB + PostGIS)
**Schema**: public

---

## 统计口径

主统计口径：
仅统计 public schema 下 `pg_class.relkind='r'` 的 ordinary BASE TABLE。
视图、物化视图、PostGIS 元数据视图不参与主统计，已写入 `excluded_objects.csv`。

---

## 关键统计

| 指标 | 数值 |
|------|------|
| 总表数 | 162 |
| 总字段数 | 3445 |
| 有表注释的表 | 143 (88.3%) |
| 有字段注释的字段 | 2863 (83.1%) |
| 缺字段注释的字段 | 582 |
| 高置信可补候选 (A档) | 4 |
| 注释冲突字段名 (B档) | 219 |
| 无法安全推断 (C档) | 310 |
| 被排除的对象 | 5 |

## 按前缀统计

| 前缀 | 表数 | 字段数 | 有注释 | 缺注释 | 覆盖率 |
|------|------|--------|--------|--------|--------|
| _stg | 3 | 42 | 0 | 42 | 0.0% |
| ad_dict | 1 | 14 | 9 | 5 | 64.3% |
| cf_auto | 1 | 7 | 7 | 0 | 100.0% |
| day_quality | 2 | 38 | 35 | 3 | 92.1% |
| dc_survey | 7 | 97 | 97 | 0 | 100.0% |
| gis_control | 1 | 12 | 12 | 0 | 100.0% |
| gis_ecologicalregion | 1 | 19 | 0 | 19 | 0.0% |
| gis_headwaters | 1 | 16 | 0 | 16 | 0.0% |
| gis_naturereserve | 1 | 25 | 0 | 25 | 0.0% |
| gis_poi | 1 | 17 | 12 | 5 | 70.6% |
| gis_region | 5 | 43 | 15 | 28 | 34.9% |
| gis_watershed | 3 | 29 | 20 | 9 | 69.0% |
| layer_boundary | 2 | 11 | 3 | 8 | 27.3% |
| layer_entity | 2 | 17 | 17 | 0 | 100.0% |
| layer_industrial | 6 | 28 | 0 | 28 | 0.0% |
| layer_outlet | 1 | 7 | 1 | 6 | 14.3% |
| layer_partition | 2 | 11 | 7 | 4 | 63.6% |
| layer_reservoir | 3 | 84 | 0 | 84 | 0.0% |
| layer_river | 2 | 46 | 0 | 46 | 0.0% |
| layer_section | 1 | 6 | 0 | 6 | 0.0% |
| layer_watershed | 1 | 4 | 0 | 4 | 0.0% |
| metadata_view | 1 | 9 | 3 | 6 | 33.3% |
| min_value | 1 | 8 | 8 | 0 | 100.0% |
| rs_enterprise | 2 | 38 | 38 | 0 | 100.0% |
| rs_industrial | 2 | 79 | 68 | 11 | 86.1% |
| rs_livestock | 1 | 68 | 68 | 0 | 100.0% |
| rs_outlet | 6 | 206 | 175 | 31 | 85.0% |
| rs_pollutant | 2 | 48 | 48 | 0 | 100.0% |
| rs_sewage | 3 | 99 | 88 | 11 | 88.9% |
| rs_warn | 1 | 25 | 25 | 0 | 100.0% |
| rs_wastewater | 4 | 193 | 193 | 0 | 100.0% |
| se_watershed | 2 | 40 | 39 | 1 | 97.5% |
| spatial_ref | 1 | 5 | 0 | 5 | 0.0% |
| stg_sjtj | 2 | 12 | 12 | 0 | 100.0% |
| stg_sjtysj | 24 | 436 | 417 | 19 | 95.6% |
| stg_sslhhpj | 6 | 97 | 97 | 0 | 100.0% |
| stg_ycsjtysj | 5 | 61 | 58 | 3 | 95.1% |
| stg_ycssthjj | 3 | 82 | 82 | 0 | 100.0% |
| wh_hydrological | 3 | 59 | 59 | 0 | 100.0% |
| wh_meteorological | 5 | 158 | 93 | 65 | 58.9% |
| wm_camera | 2 | 37 | 36 | 1 | 97.3% |
| wm_directory | 1 | 10 | 10 | 0 | 100.0% |
| wm_hydrological | 1 | 40 | 37 | 3 | 92.5% |
| wm_image | 1 | 12 | 11 | 1 | 91.7% |
| wm_meteorological | 1 | 40 | 37 | 3 | 92.5% |
| wm_panorama | 3 | 27 | 27 | 0 | 100.0% |
| wm_raster | 3 | 41 | 30 | 11 | 73.2% |
| wm_section | 2 | 36 | 36 | 0 | 100.0% |
| wm_station | 2 | 78 | 71 | 7 | 91.0% |
| wm_uav | 1 | 39 | 38 | 1 | 97.4% |
| wm_water | 5 | 152 | 134 | 18 | 88.2% |
| wm_waterbody | 1 | 27 | 18 | 9 | 66.7% |
| wm_waterquality | 5 | 341 | 339 | 2 | 99.4% |
| wst_asset | 4 | 86 | 78 | 8 | 90.7% |
| wst_control | 1 | 19 | 19 | 0 | 100.0% |
| wst_layer | 1 | 12 | 2 | 10 | 16.7% |
| wst_relation | 2 | 27 | 27 | 0 | 100.0% |
| wst_trace | 3 | 79 | 61 | 18 | 77.2% |
| wt_service | 1 | 25 | 25 | 0 | 100.0% |
| wt_warnparm | 1 | 21 | 21 | 0 | 100.0% |

## 被排除的对象

| 原因 | 数量 | 示例 |
|------|------|------|
| PostGIS 元数据视图 | 2 | geography_columns, geometry_columns |
| 视图（v_ 前缀命名规约） | 3 | v_wst_trace_edge_downstream, v_wst_trace_edge_upstream_conservative, v_wst_trace_edge_upstream_strict |

## 高置信候选 Top 20（按字段名出现次数）

| 字段名 | 缺失次数 |
|--------|---------|
| region_id | 1 |
| year | 1 |
| type_code | 1 |
| asset_id | 1 |

## 冲突字段名

共 **219** 个字段名在不同表中存在不同注释，详见 `comment_conflicts.csv`。

## 下一步建议

1. **优先处理 A 档字段**：4 个字段有库内一致注释依据，可安全批量补注释。
2. **逐个审查 B 档冲突**：219 个字段名存在注释冲突，需人工确认各表实际含义后分别补注释。
3. **业务确认 C 档字段**：310 个字段无任何库内注释参考，需 DBA / 业务方确认含义后手工补注释。
4. **表注释优先**：19 张表缺少表级注释，建议先补表注释再补字段注释。
5. **补完注释后再训练 Vanna**，不要在本阶段训练。

---

⚠️ **本报告仅做只读审计，未对数据库做任何修改。**

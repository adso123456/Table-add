# A 档二次审查程序化校验报告

**生成时间**: 2026-07-07 15:34:10
**校验脚本**: verify_review.py
**校验范围**: a_candidates_review.csv 全部 21 条 + approved/needs_manual/rejected 子文件

---

## 行数一致性

| 文件 | 行数 | 期望 |
|------|------|------|
| comment_fill_candidates.csv | 21 | 21 |
| a_candidates_review.csv | 21 | 21 |
| approved + needs_manual + rejected | 21 | 21 |
| **一致性** | **✅ 通过** | |

---

## 校验结果汇总

| 指标 | 数量 |
|------|------|
| 总行数 | 21 |
| pass | **21** |
| warn | **0** |
| fail | **0** |

### 按决策分组

| 决策 | pass | warn | fail | 小计 |
|------|------|------|------|------|
| approved | 13 | 0 | 0 | 13 |
| needs_manual | 6 | 0 | 0 | 6 |
| rejected | 2 | 0 | 0 | 2 |

---

## pass 详情

| 目标表.字段 | 决策 | 结果 |
|-------------|------|------|
| gis_region_population.region_id | needs_manual | pass |
| gis_region_population.year | needs_manual | pass |
| layer_outlet_sewage.jcdbh | approved | pass |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df.day | approved | pass |
| stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.cjsj | needs_manual | pass |
| stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.xgsj | needs_manual | pass |
| wm_hydrological_info.build_time | approved | pass |
| wm_meteorological_info.build_time | approved | pass |
| wm_raster_inversion_config.type_code | rejected | pass |
| wm_station_info.build_time | approved | pass |
| wm_waterbody_info.water_body_name | needs_manual | pass |
| wm_waterbody_info.img_name | approved | pass |
| wst_asset_trace_snap.network_type | approved | pass |
| wst_layer_river.created_at | approved | pass |
| wst_layer_river.updated_at | approved | pass |
| wst_trace_node.asset_id | needs_manual | pass |
| wst_trace_topology_issue.object_code | rejected | pass |
| wst_trace_topology_issue.created_by | approved | pass |
| wst_trace_topology_issue.created_at | approved | pass |
| wst_trace_topology_issue.updated_by | approved | pass |
| wst_trace_topology_issue.updated_at | approved | pass |

## warn 详情

| 目标表.字段 | 决策 | 结果 | 问题 |
|-------------|------|------|------|
| (无) | | | |

## fail 详情

| 目标表.字段 | 决策 | 结果 | 问题 |
|-------------|------|------|------|
| (无) | | | |

---

## 关键检查项

| 检查项 | 结果 |
|--------|------|
| approved 证据全部可溯源 | ✅ |
| 无 evidence 来自 excluded_objects | ✅ |
| 子文件与 review.csv 一致 | ✅ |
| 子文件一致性问题 | 无 |
| approved 全部 pass | ✅ |

---

## 是否可以进入下一阶段

## ✅ 可进入下一阶段



---

⚠️ **本报告仅做程序化校验，未对数据库做任何修改，未生成任何 SQL。**

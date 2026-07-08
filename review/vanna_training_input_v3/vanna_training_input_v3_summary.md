# Vanna 训练输入清单 V3

**生成时间**: 2026-07-08 15:12:38
**数据源**: metadata_snapshot_v3
**状态**: 清单已生成，未训练 Vanna

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| 总表数 | 162 |
| 可训练表 | 115 |
| 排除表 | 47 |
| 总字段数 | 3445 |
| 可训练字段 | 2572 |
| 排除字段 | 873 |

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
| **合计** | **47** |

### 排除表清单

| 表 | 列数 | 有注释 | 排除原因 |
|-----|------|--------|----------|
| _stg_yichang_river_counts | 5 | 0 | 临时导入表，数据不稳定且字段语义未经业务确认; 无表注释且字段注释覆盖率仅 0%，训练上下文不足; 全字段无注释，无可用 |
| _stg_yichang_river_import | 27 | 21 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| _stg_yichang_river_std | 10 | 9 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| layer_river_provincial_bak0617 | 23 | 17 | 备份表，与主表重复，训练价值低 |
| rs_industrial_info_yc_bak0305 | 13 | 13 | 备份表，与主表重复，训练价值低 |
| spatial_ref_sys | 5 | 5 | PostGIS 系统表，非业务数据 |
| stg_sjtj_sxhysjzxpt_dbo_operator_day_burnup_df | 4 | 4 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtj_sxhysjzxpt_t_vessel_info_df | 8 | 8 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_clean_company_df | 4 | 4 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df | 15 | 15 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_clean_company_df | 15 | 15 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_coordination_index_df | 9 | 9 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_pollution_weight_df | 15 | 15 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df | 11 | 11 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_subject_num_df | 8 | 8 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_sxhy_df | 10 | 10 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_month_receive_ship_kpi_df | 20 | 20 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_order_receive_minute_df | 8 | 8 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_process_unit_info_df | 19 | 19 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_receive_ship_assessment_df | 13 | 13 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_receive_ship_info_df | 22 | 22 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_transfer_car_df | 12 | 12 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_wharf_info_df | 20 | 20 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_b_wharf_kpi_df | 9 | 9 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_apply_detail_df | 16 | 16 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_ashore_apply_df | 64 | 56 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_handover_trans_detail_df | 8 | 5 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_handover_trans_df | 31 | 31 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_receive_storage_df | 5 | 5 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_trans_apply_detail_df | 5 | 5 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_trans_apply_df | 72 | 72 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sjtysj_cbwrwxtzlxxxt_p_wharf_storage_df | 25 | 25 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_att_bas_base_df | 21 | 21 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_att_wmst_base_df | 28 | 28 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_rcm_rv_lk_res_df | 15 | 15 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_rel_st_source_df | 3 | 3 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_warn_stcd_r_df | 6 | 6 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_sslhhpj_hbsxkqycszhslzhglptjsxm_wr_mp_b_df | 24 | 24 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycsjtysj_sxhyzssj_base_channel_df | 9 | 9 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycsjtysj_sxhyzssj_base_channel_level_df | 10 | 10 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycsjtysj_sxhyzssj_base_ship_df | 18 | 17 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycsjtysj_sxhyzssj_data_coverage_wharf_df | 13 | 13 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycsjtysj_sxhyzssj_data_ship_info_df | 11 | 11 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycssthjj_ltwsjgpt_t_sjzx_wry_jbxx_df | 47 | 47 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycssthjj_lysthjjkyjpt_t_sjzx_szzdjcz_df | 12 | 12 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df | 23 | 23 | 临时导入表，数据不稳定且字段语义未经业务确认 |
| wm_water_source_bak0421 | 61 | 61 | 备份表，与主表重复，训练价值低 |


---

## 四、输出文件

| 文件 | 行数 |
|------|------|
| `vanna_trainable_tables_v3.csv` | 115 |
| `vanna_trainable_columns_v3.csv` | 2572 |
| `vanna_excluded_objects_v3.csv` | 920 |
| `vanna_training_input_v3_summary.md` | 本文件 |

---

## 五、边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未编造注释
> - ❌ 所有训练字段均使用数据库真实注释

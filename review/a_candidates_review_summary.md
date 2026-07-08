# A 档候选二次审查报告

**生成时间**: 2026-07-07 15:29:06
**审查范围**: comment_fill_candidates.csv 全部 21 条
**审查方式**: 逐条人工复核，基于证据表域、字段语义、跨域风险判断

---

## 审查结果

| 决策 | 数量 |
|------|------|
| approved (批准) | 13 |
| needs_manual (需人工确认) | 6 |
| rejected (拒绝) | 2 |
| **合计** | **21** |

---

## 批准详情

| 目标表.字段 | 证据数 | 批准理由 |
|-------------|--------|----------|
| layer_outlet_sewage.jcdbh | 2 | evidence_count=2 + 同属排污/废水排放业务域 + jcdbh(监测点编号)拼音缩写与证据表语义一致 + 目标表为排放口图层，监测点编号是核心标识 |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df.day | 5 | evidence_count=5 + 全部同一 staging 模块(stg_sjtysj) + 目标表和证据表均为同一数据源系统的日统计类表 + day 字段语义一致 |
| wm_hydrological_info.build_time | 1 | 同属 wm 站点/水文业务域 + 目标表(水位站)与证据表(自动站点)均为监测站点类表 + build_time 语义明确为建设时间 + 同模块同语义 |
| wm_meteorological_info.build_time | 1 | 同属 wm 站点体系 + 目标表(气象监测站)与证据表(自动站点)均为监测站点类表 + build_time 语义一致 |
| wm_station_info.build_time | 1 | 同表族(v1/v2) + 目标表与证据表为同一业务对象的两个版本 + build_time 语义绝对一致 |
| wm_waterbody_info.img_name | 3 | evidence_count=3 + 全部 wm 域 + 目标表为水体信息表，照片名称是合理的附属信息字段 + 多表一致注释为'照片名称' |
| wst_asset_trace_snap.network_type | 2 | evidence_count=2 + 全部 wst 域 + 目标表(资产追溯挂接)与证据表(追溯边/节点)同属 pgRouting 拓扑追溯模块 + network_type 枚举值完全一致 |
| wst_layer_river.created_at | 9 | evidence_count=9 + 全部 wst 域 + created_at 为标准通用审计字段 + 库内注释完全一致为'创建时间' |
| wst_layer_river.updated_at | 9 | evidence_count=9 + 全部 wst 域 + updated_at 为标准通用审计字段 + 库内注释完全一致为'更新时间' |
| wst_trace_topology_issue.created_by | 6 | evidence_count=6 + 全部 wst 域 + created_by 为标准通用审计字段 + 库内注释完全一致为'创建人' |
| wst_trace_topology_issue.created_at | 9 | evidence_count=9 + 全部 wst 域 + created_at 为标准通用审计字段 + 库内注释完全一致 |
| wst_trace_topology_issue.updated_by | 6 | evidence_count=6 + 全部 wst 域 + updated_by 为标准通用审计字段 + 库内注释完全一致为'更新人' |
| wst_trace_topology_issue.updated_at | 9 | evidence_count=9 + 全部 wst 域 + updated_at 为标准通用审计字段 + 库内注释完全一致 |

## 需人工确认

| 目标表.字段 | 风险 | 确认问题 |
|-------------|------|----------|
| gis_region_population.region_id | medium | gis_region_population 的 region_id 是否与 wm_section_info 的 '所属区域id' 指向同一区域编码体系？ |
| gis_region_population.year | medium | gis_region_population 的 year 字段代表什么年份(统计年份?数据年份?)? |
| stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.cjsj | low | cjsj 在该 staging 表中是否确实代表'创建时间'？ |
| stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.xgsj | low | xgsj 在该 staging 表中是否确实代表'修改时间'？ |
| wm_waterbody_info.water_body_name | low | wm_waterbody_info 的 water_body_name 是否确实代表'水体名称'？(语义自明，确认即可) |
| wst_trace_node.asset_id | medium | wst_trace_node.asset_id 是否关联 wst_asset.id？ |

## 拒绝详情

| 目标表.字段 | 拒绝理由 |
|-------------|----------|
| wm_raster_inversion_config.type_code | 跨业务域严重不匹配 - 目标表为 wm_raster(栅格反演配置)，证据表为 wst_relation_type_dict(关系大类字典) + type_code 在栅格配置上下文中不可能表示 '关系大类编码' + 字段语义完全不匹配 |
| wst_trace_topology_issue.object_code | 跨业务域严重不匹配 - 目标表为 wst_trace(水安全追溯模块)，证据表为 stg_sslhhpj(第三方项目 staging 表) + object_code 在拓扑问题表中极可能表示拓扑错误对象编码而非监控对象编码 |

---

## 关键发现

1. **标准审计字段 (created_at/updated_at/created_by/updated_by)** 表现最好：5 条候选均来自 wst 域、多表一致注释，全部批准。
2. **build_time** 在 wm 站点体系内语义一致（3 条批准）：水位站、气象站、水质站的 build_time 均为"建设时间"。
3. **跨域误匹配是主要拒绝原因**：type_code(wm_raster vs wst_relation) 和 object_code(wst_trace vs stg) 两条因业务域完全不匹配被拒绝。这表明上一阶段 A 档分类算法存在跨域误报风险。
4. **拼音缩写字段 (cjsj/xgsj/jcdbh)** 需要区别对待：jcdbh 因证据明确且同域获批，cjsj/xgsj 因单证据降级为人工确认。
5. **evidence_count=1 的非审计字段** (region_id/year/water_body_name/asset_id) 全部降级为人工确认，按规则严格执行。

## 候选污染评估

- 2 条被拒绝（占比 9.5%），均因跨业务域错误匹配
- 6 条需人工确认，其中 4 条大概率可通过人工快速确认为 approved
- 13 条批准（占比 61.9%），均为有充分库内证据支持的低风险候选

## 下一步建议

1. **批准 13 条可立即进入补注释队列**（但本阶段不执行补库）
2. **needs_manual 的 6 条**建议由 DBA/业务方按 manual_check_question 逐条确认后升级为 approved
3. **rejected 的 2 条**应从补注释计划中移除，由业务方独立定义注释
4. **改进 A 档分类算法**：在 run_metadata_audit.py 中增加跨业务域前缀检查，避免 wm/wst/gis/stg 之间的 evidence 跨域传播

---

⚠️ **本报告仅做审查分析，未对数据库做任何修改，未生成任何 SQL。**

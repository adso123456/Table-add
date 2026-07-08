# batch_001 人工审核建议 V2 — 汇总

**生成时间**: 2026-07-08
**版本**: V2
**范围**: `batch_001` / `wm_raster_inversion` 全部 10 个字段
**状态**: 建议已生成，review_decision 全部留空，待人工填写

---

## 一、审核对象

| 项目 | 值 |
|------|-----|
| 批次 | batch_001 |
| 表 | wm_raster_inversion |
| 表注释 | 遥感反演结果表（合并版） |
| 字段数 | 10 |
| review_decision 状态 | 全部留空 |

---

## 二、建议分布

| 建议类型 | 数量 | 字段 |
|----------|------|------|
| `suggest_exclude_from_training` | 1 | record_id |
| `suggest_possible_limited_training` | 7 | inversion_type, l1_area, l2_area, l3_area, l4_area, l5_area, l6_area |
| `suggest_hold_for_business_review` | 2 | service_url, data_time |

---

## 三、当前状态与 V1 对比

| 指标 | V1 | V2 |
|------|-----|-----|
| 表注释 | 缺失 | 遥感反演结果表（合并版） |
| record_id 注释 | 误填（表级描述） | 已修正 |
| missing_table_comment | 10 行 | 0 行 |
| 可建议训练字段 | 0（全部受阻于 missing_table_comment） | 7（inversion_type + l1~l6） |
| 需业务确认字段 | 2 | 2 |
| 建议排除字段 | 1 | 1 |

---

## 四、文件清单

| 文件 | 用途 |
|------|------|
| `batch_001_human_review_assist_v2.csv` | 审核辅助建议（含 risk_reason + suggested_review_tendency） |
| `batch_001_human_decision_template_v2.csv` | 审核决策模板（review_decision 留空，待人工填写） |
| `batch_001_human_review_notes_v2.md` | 详细审核说明 |
| `batch_001_human_review_summary_v2.md` | 本汇总文件 |

---

## 五、下一步

1. 人工审核 `batch_001_human_review_assist_v2.csv` 中每条建议
2. 在 `batch_001_human_decision_template_v2.csv` 中填写 `review_decision`
3. 确认后进入训练准备阶段

---

## 六、阶段边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未修改旧版 human_review 文件
> - ❌ 未自动填写 review_decision
> - ❌ 未修改项目代码

# wm_raster_inversion 注释对齐候选包 — 生成摘要

**生成时间**: 2026-07-08

---

## 1. 读取了哪些文件

| 文件 | 用途 |
|------|------|
| `batch_001_review_template.csv` | 10 条字段审核模板 |
| `batch_001_suspicious_focus.csv` | 15 条可疑项 |
| `batch_001_human_review_assist.csv` | 建议倾向（确认 record_id 注释异常） |
| `batch_001_human_decision_template.csv` | 决策模板（参考） |
| `batch_001_human_review_summary.md` | 审核包摘要 |

---

## 2. 生成了哪些文件

| 文件 | 说明 |
|------|------|
| `wm_raster_inversion_comment_alignment_candidate.csv` | 2 条注释对齐候选（含证据和风险评估） |
| `wm_raster_inversion_comment_alignment_decision_template.csv` | 2 条人工决策模板（human_decision 留空） |
| `wm_raster_inversion_comment_alignment_notes.md` | 人工确认说明 |
| `wm_raster_inversion_comment_alignment_summary.md` | 本文件 |

---

## 3. 表级注释候选数量

**1** 条：`wm_raster_inversion` 表注释候选 → `遥感反演结果表（合并版）`

## 4. 字段注释修正候选数量

**1** 条：`record_id` 注释候选 → `遥感反演结果记录ID`

## 5. 其他字段是否保持不变

**是。** `inversion_type`、`l1_area`–`l6_area`、`service_url`、`data_time` 共 9 个字段的注释不提出修改候选。
其中 `inversion_type` + `l1_area`–`l6_area` 注释质量较好，`service_url` 和 `data_time` 证据不足不编造。

---

## 6. human_decision 是否全部留空

**是。** 两个模板中所有 `human_decision` 和 `human_note` 均为空。

---

## 7. 是否修改数据库

**否。** 未连接数据库，未执行任何 DDL。

## 8. 是否执行 SQL

**否。** 本阶段未生成任何 SQL。

## 9. 是否训练 Vanna

**否。** 未调用任何 Vanna API。

## 10. 是否写入 vanna_data / agent_data

**否。** 所有输出在 `batches/batch_001_comment_alignment/` 下。

---

## 11. 是否可以进入人工确认阶段

**可以进入人工确认 wm_raster_inversion 注释对齐候选阶段，但仍不能执行 SQL，不能训练 Vanna。**

说明：
- 2 条候选已生成，含证据和风险评估
- 所有 human_decision 已留空，等待人工填写
- 候选涉及修改已有注释（record_id），必须单独人工确认
- 其他 9 个字段注释保持不变

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 表级注释候选 1 条 | 是 |
| 字段注释修正候选 1 条 | 是 |
| 其他 9 字段不变 | 是 |
| human_decision 全部留空 | 是 |
| 未执行 SQL | 是 |
| 未修改数据库 | 是 |
| 未改造已有注释 | 是 |
| 未编造 service_url/data_time 含义 | 是 |
| 未训练 Vanna | 是 |
| 未写入 vanna_data / agent_data | 是 |
| 未修改项目代码 | 是 |


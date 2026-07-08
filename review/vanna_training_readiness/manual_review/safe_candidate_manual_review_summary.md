# Safe Candidate 人工审核包 — 生成摘要

**生成时间**: 2026-07-08

---

## 1. safe_candidate_only 总数

- **1451** 条安全训练候选字段
- 涉及 **128** 张表

---

## 2. 按表汇总

| 指标 | 数值 |
|------|------|
| 表总数 | 128 |
| safe_candidate 总字段数 | 1451 |

---

## 3. 审核优先级分布

| 优先级 | 表数 | 说明 |
|--------|------|------|
| high | 1 | 表注释缺失或字段数多，需优先审核 |
| medium | 14 | 有部分风险因素 |
| low | 113 | 表注释清楚，字段注释明确 |

---

## 4. suspicious items 数量

- **总计**: 1039 条建议重点审核
- 分布:
  - very_short_comment: 614
  - code_like_field: 104
  - name_like_field: 93
  - id_like_field: 52
  - generic_comment: 49
  - status_like_field: 46
  - time_like_field: 46
  - missing_table_comment: 33
  - business_sensitive_field: 2

> 注意：suspicious 不等于错误，仅表示建议人工重点审核。

---

## 5. review_decision 状态

**全部留空。** `safe_candidate_field_review_template.csv` 中 1451 条记录的 `review_decision` 均为空，待人工逐字段填写。

---

## 6. 原始注释保留

- 所有 `column_comment` 从 `vanna_training_safe_candidate_only.csv` 直接复制
- 未做 trim / strip / normalize
- 前导空格、末尾空格、换行符均保留
- 与 `columns_with_comments.csv` 原文完全一致

---

## 7. 是否训练 Vanna

**否。** 本阶段未调用任何 Vanna API，未生成训练数据。

---

## 8. 是否写入 vanna_data / agent_data

**否。** 所有输出在 `review/vanna_training_readiness/manual_review/` 下。

---

## 9. 是否可以进入人工审核阶段

**可以进入人工审核 safe_candidate_only 白名单阶段，但仍不能训练 Vanna。**

理由：
- 审核包已生成，所有模板和可疑标记已就绪
- review_decision 全部留空，等待人工填写
- 注释保留原文，未做任何修改
- 但仍需人工逐字段审核后才能进入受限训练准备

---

## 10. 下一步建议（不要在本阶段执行）

1. 打开 `safe_candidate_table_summary.csv`，按 review_priority 排序
2. 先审核 high 优先级表的字段
3. 参考 `safe_candidate_suspicious_items.csv` 标记的可疑项
4. 在 `safe_candidate_field_review_template.csv` 中填写 review_decision
5. 审核完成后统计结果，仅 `approve_for_limited_training` 的字段进入训练准备
6. **审核阶段仍不训练 Vanna**

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 审核包包含 1451 条字段 | 是 |
| 涉及 128 张表 | 是 |
| review_priority: high=1, medium=14, low=113 | 是 |
| suspicious_items=1039 条 | 是 |
| review_decision 全部留空 | 是 |
| 未自动批准任何字段 | 是 |
| 原始注释保留原文 | 是 |
| 未训练 Vanna | 是 |
| 未写入 vanna_data / agent_data | 是 |
| 未修改数据库 | 是 |
| 未修改项目代码 | 是 |


# batch_001 人工审核指南

**生成时间**: 2026-07-08

---

## 1. 第 1 批概况

| 指标 | 数值 |
|------|------|
| 字段数量 | 10 |
| 表数量 | 1 |
| 表名 | wm_raster_inversion |
| table_comment | 空（缺失） |
| suspicious 数量 | 15 |

---

## 2. 审核时重点看什么

1. **表级上下文缺失**：该表无 table_comment，审核前先了解该表的业务用途
2. **注释准确性**：逐字段确认 column_comment 是否正确描述字段含义
3. **可疑项优先**：先打开 `batch_001_suspicious_focus.csv` 查看标记的可疑项
4. **字段类型匹配**：确认 data_type 与注释描述的业务含义是否匹配
5. **业务相关性**：该字段是否适合用于 Text-to-SQL 训练

---

## 3. review_decision 三个允许值

| 值 | 含义 | 何时使用 |
|------|------|----------|
| `approve_for_limited_training` | 批准在带表上下文的条件下训练 | 注释准确、业务含义明确 |
| `hold_for_business_review` | 暂缓，需业务方确认 | 注释不明确、可疑、或业务含义不确定 |
| `exclude_from_training` | 排除，不纳入训练 | 注释错误、字段含义不清、或不适合训练 |

---

## 4. 不确定时怎么填

**填写 `hold_for_business_review`。**

宁可暂缓也不要随便 approve。一个错误 approve 的注释会污染 Text-to-SQL 模型的该字段理解。

---

## 5. 禁止事项

1. 不要为了推进训练随便填 `approve_for_limited_training`
2. 不要修改 `column_comment` 的值
3. 不要在审核阶段训练 Vanna
4. 不要跳过可疑项
5. 不要在审核包中直接改注释文本

---

## 6. 审核步骤建议

1. 打开 `batch_001_review_template.csv`
2. 先浏览 `batch_001_suspicious_focus.csv` 了解全部可疑项
3. 逐字段填写 `review_decision`
4. 如有疑问，在 `review_note` 中记录原因
5. 审核完成后保存文件
6. **审核阶段仍不训练 Vanna**


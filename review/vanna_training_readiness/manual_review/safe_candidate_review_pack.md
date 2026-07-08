# Safe Candidate 白名单人工审核包

**生成时间**: 2026-07-08
**状态**: 只读生成，未训练 Vanna

---

## 1. 本阶段目的

对 `vanna_training_safe_candidate_only.csv`（1451 条安全训练候选）生成结构化人工审核包，供业务方/DBA 逐字段审核后再决定是否纳入受限训练。

**本阶段只生成白名单人工审核包，不训练 Vanna，不写入 vanna_data / agent_data。**

---

## 2. 读取的文件

| 文件 | 用途 |
|------|------|
| `vanna_training_safe_candidate_only.csv` | 1451 条 safe candidate |
| `tables_summary.csv` | 表级统计信息 |
| `columns_with_comments.csv` | 原始注释源文件 |
| `vanna_training_readiness_summary.md` | 清单生成口径 |
| `vanna_training_lists_verify_summary.md` | V1–V20 校验结果 |
| `vanna_training_comment_integrity_summary.md` | 注释完整性校验 |

---

## 3. safe_candidate_only 数量

- **总字段数**: 1451
- **涉及表数**: 128
- **列注释均保留原文**: 是
- **注释完整性校验 V1–V20**: 全部 PASS

---

## 4. 为什么仍不能直接训练

虽然这 1451 个字段无同名字段冲突、且有注释，但存在以下风险：

1. **注释质量不确定**：部分注释可能过于通用（如 `id` → `主键`），缺乏业务语义
2. **表级上下文缺失**：部分表无 table_comment，模型可能误解字段用途
3. **注释准确性未验证**：注释由 DBA/开发人员填写，可能存在错误或过时
4. **业务敏感字段**：空间几何字段、加密字段等需确认是否适合训练
5. **未经人工审核的训练数据会放大错误**：一个错误注释可能污染模型对该字段类型的理解

---

## 5. 人工审核需要看什么

| 审核维度 | 检查内容 | 产出 |
|----------|----------|------|
| 注释准确性 | column_comment 是否正确描述字段含义 | approve / hold / exclude |
| 表级上下文 | table_comment 是否完整，是否提供足够业务背景 | 是否需要先补表注释 |
| 字段通用性 | 注释是否过于通用（如 `主键`、`状态`） | 是否需要补充业务含义 |
| 业务敏感度 | 字段是否包含业务敏感数据 | 是否排除训练 |
| 数据类型匹配 | data_type 与注释是否一致 | 注释是否与物理类型匹配 |

---

## 6. 原始注释保护原则

- 本审核包中所有 `column_comment` 来自 `columns_with_comments.csv` 原文
- 未做 strip / trim / normalize / 改写
- 审核过程中发现注释错误，不应在本阶段修改——应标记为 `hold_for_business_review`
- 注释修改必须走独立的 COMMENT ON COLUMN 流程，不得在审核包中直接改

---

## 7. 禁止事项

1. 禁止直接将 1451 条标记为 `approved_for_training`
2. 禁止基于猜测批量批准
3. 禁止在审核包中直接修改 column_comment
4. 禁止跳过人工审核直接训练
5. 禁止把 suspicious_items 直接当错误删除

---

## 8. 后续人工审核流程

1. 打开 `safe_candidate_field_review_template.csv`
2. 逐字段填写 `review_decision`：
   - `approve_for_limited_training`：注释准确，可在带表上下文的条件下训练
   - `hold_for_business_review`：注释不明确或可疑，需业务方确认
   - `exclude_from_training`：不应纳入训练
3. 优先审核 `safe_candidate_suspicious_items.csv` 中的可疑项
4. 优先审核 review_priority=high 的表
5. 审核完成后统计 approve / hold / exclude 数量
6. 仅 `approve_for_limited_training` 的字段可进入后续受限训练准备
7. **审核阶段仍不训练 Vanna**

---

## 9. 审核包文件清单

| 文件 | 说明 |
|------|------|
| `safe_candidate_review_pack.md` | 本文件，审核说明 |
| `safe_candidate_table_summary.csv` | 按表汇总，含审核优先级 |
| `safe_candidate_field_review_template.csv` | 1451 条待审核字段模板，review_decision 留空 |
| `safe_candidate_suspicious_items.csv` | 1039 条建议重点审核项 |
| `safe_candidate_manual_review_summary.md` | 审核包生成摘要 |

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 未训练 Vanna | 是 |
| 未写入 vanna_data | 是 |
| 未写入 agent_data | 是 |
| 未修改数据库 | 是 |
| 未修改原始注释 | 是 |
| review_decision 全部留空 | 是 |
| 未自动批准任何字段 | 是 |
| 覆盖 128 张表 | 是 |


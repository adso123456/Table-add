# wm_raster_inversion 衍生文件刷新报告

**刷新时间**: 2026-07-08
**状态**: 刷新完成，未训练 Vanna

---

## 一、刷新的文件

| # | 文件 | 刷新内容 | 修改行数 |
|---|------|----------|----------|
| 1 | `columns_with_comments.csv` | record_id 注释：旧→新 | 1 |
| 2 | `vanna_training_safe_candidate_only.csv` | record_id 注释：旧→新 | 1 |
| 3 | `batch_001_review_template.csv` | record_id 注释 + 移除 missing_table_comment | 1 + 10 |

**共修改 13 处。**

---

## 二、刷新详情

### 2.1 record_id 注释（3 处）

| 文件 | 行号 | 旧值 | 新值 |
|------|------|------|------|
| `columns_with_comments.csv` | 2516 | 遥感反演结果表（合并版） | 遥感反演结果记录ID |
| `vanna_training_safe_candidate_only.csv` | 1083 | 遥感反演结果表（合并版） | 遥感反演结果记录ID |
| `batch_001_review_template.csv` | 2 | 遥感反演结果表（合并版） | 遥感反演结果记录ID |

### 2.2 missing_table_comment 移除（10 处）

`batch_001_review_template.csv` 中 wm_raster_inversion 全部 10 行移除了 `missing_table_comment` 标记：

| 行号 | 字段 | 修改前 | 修改后 |
|------|------|--------|--------|
| 2 | record_id | `id_like_field \| missing_table_comment` | `id_like_field` |
| 3 | inversion_type | `code_like_field \| missing_table_comment` | `code_like_field` |
| 4-9 | l1_area ~ l6_area | `missing_table_comment` | (空) |
| 10 | service_url | `missing_table_comment \| very_short_comment` | `very_short_comment` |
| 11 | data_time | `missing_table_comment \| time_like_field \| very_short_comment` | `time_like_field \| very_short_comment` |

---

## 三、未修改的关联文件（过期清单）

以下文件仍含旧注释 `遥感反演结果表（合并版）`，属于历史快照或其他批次，本次未修改：

| 文件 | 状态 |
|------|------|
| `vanna_training_comment_integrity_report.csv` | 行 2053, 4020 — 旧注释 |
| `vanna_training_candidate_whitelist.csv` | 行 2016 — 旧注释 |
| `batch_001_suspicious_focus.csv` | 行 2-3 — 旧注释 |
| `safe_candidate_field_review_template.csv` | 行 1083 — 旧注释 |
| `safe_candidate_suspicious_items.csv` | 行 738-739 — 旧注释 |
| `batch_001_human_review/batch_001_human_decision_template.csv` | 行 2 — 旧注释 |
| `batch_001_human_review/batch_001_human_review_assist.csv` | 行 2 — 旧注释 |
| `batch_001_comment_alignment/` 下所有文件 | 历史快照，无需修改 |

---

## 四、自查确认

| 检查项 | 结果 |
|--------|------|
| 只改 wm_raster_inversion 相关行 | ✅ |
| record_id 旧注释已消失 | ✅ 在 3 个目标文件中已全部刷新 |
| 表级 missing_table_comment 已移除 | ✅ 10 行全部移除 |
| 未改其他字段注释 | ✅ 抽查 indicator_code, inversion_type, l1_area 均未变 |
| 未 trim / strip / normalize | ✅ 精准匹配替换 |
| 未训练 Vanna | ✅ |
| 未修改数据库 | ✅ |

---

## 五、阶段边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未执行 SQL
> - ❌ 未修改项目代码

# Vanna 训练 readiness 评估 — 白名单/排除清单/冲突观察清单（修正版）

**生成时间**: 2026-07-07
**修正时间**: 2026-07-07
**二次修正时间**: 2026-07-08
**二次修正原因**: 生成脚本对 column_comment 使用了 .strip()，导致白名单注释丢失前导空格、末尾空格、末尾换行符，违反原始注释保护规则
**状态**: 只读生成清单，未训练 Vanna

---

本阶段仍不训练 Vanna。仅生成训练候选白名单、排除清单和冲突观察清单。

---

## 1. 本阶段读取的文件

| 文件 | 用途 |
|------|------|
| `columns_with_comments.csv` | 3445 字段注释状态 |
| `missing_comments.csv` | 582 缺注释字段 |
| `comment_conflicts.csv` | 219 冲突字段名 |
| `comment_fill_candidates.csv` | 4 条剩余 A 档候选 |
| `unsafe_unfilled_columns.csv` | 310 条 C 档 unsafe |
| `excluded_objects.csv` | 5 个排除对象 |

---

## 2. 是否训练 Vanna

**否。** 本阶段未调用任何 Vanna API。

---

## 3. 是否写入 vanna_data / agent_data

**否。** 所有输出在 `review/vanna_training_readiness/` 下。

---

## 4. 白名单生成规则

| 规则 | 说明 |
|------|------|
| 来源 | `columns_with_comments.csv` 中 has_comment=True |
| training_status 分类 | candidate_safe（无冲突）/ candidate_with_conflict_warning（字段名在冲突列表） |
| 原始注释保护 | 不改写、不润色、不统一任何已有注释 |
| 排除 | missing / unsafe / keep_manual / reject / excluded_objects 表 |

---

## 5. 排除清单生成规则

按优先级分类，B 档冲突字段名以 `table_name=*` 纳入：

| 优先级 | 分类 | 数量 |
|--------|------|------|
| 1 | conflict_same_name_different_meaning | **219** |
| 2 | rejected_candidate | 1 |
| 3 | keep_manual | 3 |
| 4 | unsafe_no_evidence（C 档） | 310 |
| 5 | missing_comment（其余缺注释） | 268 |

---

## 6. 冲突 watchlist 生成规则

| 规则 | 说明 |
|------|------|
| 来源 | `comment_conflicts.csv` 219 条 |
| 原则 | 不改写原始注释，不统一注释，不选择"正确"注释 |
| 训练建议 | 如需训练，必须带 table_name / table_comment / schema context |
| 同时进入 | conflict_watchlist + exclusion/risk list |

---

## 7. 原始注释保护原则

- 白名单中 column_comment 为原始注释文本，未经任何修改
- 不因统一风格而改写已有注释
- 冲突字段保留各自原始注释，不选"统一版本"
- B 档冲突只标记风险，不修改、不覆盖原始注释

### 7.1 注释保留修复（2026-07-08）

**问题**：`generate_vanna_training_lists.py` 第 148 行对 `column_comment` 调用了 `.strip()`，导致写入白名单时丢失了注释中的前导空格、末尾空格和末尾换行符。

**修复**：
- 第 148–151 行：改为 `source_comment = r.get("column_comment", "")` + `if not source_comment.strip(): continue`，仅用 strip 判断非空，不修改原文
- 第 173 行：`"column_comment": source_comment` 写原文，不再写 strip 后的值
- `read_csv()`：添加 `newline=""` 确保 CSV 字段中的嵌入换行符被正确读取

**原则**：
- 白名单中的 `column_comment` 保留 `columns_with_comments.csv` 原文
- 未做 strip / trim / normalize
- 注释中的前导空格、末尾空格、换行符均按原文保留
- 仅用 `.strip()` 做非空判断，不改变写入值

### 7.2 原始注释完整性校验（2026-07-08）

校验脚本 `verify_vanna_training_lists.py` 新增 V16–V20 共 5 条逐字段注释一致性规则：

| 规则 | 说明 | 结果 |
|------|------|------|
| V16 | whitelist 注释逐行一致（vs columns_with_comments.csv） | PASS，mismatch=0 |
| V17 | safe_candidate_only 注释逐行一致（vs columns_with_comments.csv） | PASS，mismatch=0 |
| V18 | whitelist 字段均能回源 columns_with_comments.csv | PASS，missing_source=0 |
| V19 | safe_candidate_only 字段均能回源 columns_with_comments.csv | PASS，missing_source=0 |
| V20 | 原始注释未改写结论 | PASS |

**完整性校验结论**：原始注释逐字段完整性校验通过（V1–V20 全部 PASS），未发现白名单改写原始注释。

---


## 8. 关键数据口径（修正版）

| 指标 | 数值 |
|------|------|
| raw_has_comment_count（候选池总量） | **2863** |
| candidate_safe_count（安全训练候选） | **1451** |
| candidate_with_conflict_warning_count（冲突警示候选） | **1412** |
| safe_candidate_only_count（safe only 文件） | **1451** |
| conflict_watch_count（冲突字段名） | **219** |
| exclusion_total_count | **801** |
| └ conflict_same_name_different_meaning | 219 |
| └ missing_comment | 268 |
| └ unsafe_no_evidence | 310 |
| └ keep_manual | 3 |
| └ rejected_candidate | 1 |

---

## 9. 口径说明（修正版）

**2863 个有注释字段是 raw candidate pool，不是全部可安全训练。**

- **1451** 个字段（50.7%）无冲突 → `candidate_safe` → 写入 `vanna_training_safe_candidate_only.csv` → 后续人工审核基础
- **1412** 个字段（49.3%）有冲突 → `candidate_with_conflict_warning` → 不能直接训练，训练时必须带表级上下文
- **219** 个冲突字段名已同时进入：
  - `vanna_training_conflict_watchlist.csv`（冲突观察）
  - `vanna_training_exclusion_list.csv`（排除/风险清单，`conflict_same_name_different_meaning`）
- **582** 个缺注释字段已全部排除
- B/C/keep_manual/reject 已全部标记

---

## 10. 是否可以进入训练

**可以进入"训练前人工审核 safe_candidate_only 白名单"阶段，但仍不能直接训练。**

理由：
- `vanna_training_safe_candidate_only.csv` 已生成（1451 条安全候选）
- B 档冲突已纳入 exclusion list（219 条）
- 排除清单完整覆盖 801 条（含 582 缺注释 + 219 冲突）
- 冲突观察清单 219 条已标记风险
- 但仍需人工审核 safe_candidate_only 白名单后再进入受限训练准备

---

## 11. 生成文件清单

| 文件 | 行数 | 说明 |
|------|------|------|
| `vanna_training_candidate_whitelist.csv` | 2863 | raw 候选池（safe + conflict_warning） |
| `vanna_training_safe_candidate_only.csv` | 1451 | **仅 safe，后续人工审核基础** |
| `vanna_training_exclusion_list.csv` | 801 | 排除清单（含 B 档冲突） |
| `vanna_training_conflict_watchlist.csv` | 219 | 冲突字段名观察清单 |
| `vanna_training_comment_integrity_report.csv` | — | 逐字段注释比对详情（match/mismatch/missing_source） |
| `vanna_training_comment_integrity_summary.md` | — | 注释完整性校验中文摘要 |
| `vanna_training_lists_verify_report.csv` | — | V1–V20 逐条校验结果 |
| `vanna_training_lists_verify_summary.md` | — | V1–V20 校验报告摘要 |

---

## 12. 下一步建议（不要在本阶段执行）

1. 人工审核 `vanna_training_safe_candidate_only.csv`（1451 条）
2. 人工审核 `vanna_training_exclusion_list.csv` 中的 219 条 conflict 风险项
3. 确认是否需要调整 conflict 字段的处理策略
4. 审核通过后进入受限训练准备阶段
5. **不要在本阶段训练 Vanna**

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 未训练 Vanna | 是 |
| 未写入 vanna_data | 是 |
| 未写入 agent_data | 是 |
| 未修改数据库 | 是 |
| 未修改原始注释 | 是 |
| 未改写原始注释（未 strip / trim / normalize） | 是 |
| 原始注释完整性校验 V1–V20 全部通过 | 是 |
| B 档冲突已同时进入 exclusion + watchlist | 是 |
| safe_candidate_only 不含 conflict_warning | 是 |
| 未写"可以直接训练" | 是 |

---

⚠️ **本阶段只生成清单，不训练 Vanna，不修改数据库，不补注释。**

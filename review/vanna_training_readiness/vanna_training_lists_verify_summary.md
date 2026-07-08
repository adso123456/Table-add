# Vanna 训练 readiness 清单校验报告

**校验时间**: 2026-07-08

## 汇总

| 指标 | 数值 |
|------|------|
| 总规则数 | 20 |
| PASS | 20 |
| FAIL | 0 |

## 逐条结果

| 规则 | 说明 | 结果 | 详情 |
|------|------|------|------|
| V1 | candidate_whitelist = 2863 | PASS | actual 2863 |
| V2 | candidate_safe = 1451 | PASS | actual 1451 |
| V3 | candidate_with_conflict_warning = 1412 | PASS | actual 1412 |
| V4 | conflict_watchlist = 219 | PASS | actual 219 |
| V5 | safe_candidate_only = 1451 | PASS | actual 1451 |
| V6 | safe_only 不含 candidate_with_conflict_warning | PASS | found 0 |
| V7 | safe_only 不含 conflict_watchlist 中的字段名 | PASS | found 0 |
| V8 | exclusion 含 219 条 conflict_same_name_different_meaning | PASS | actual 219 |
| V9 | missing_comments 不进入 safe_only | PASS | found 0 |
| V10 | unsafe C档 不进入 safe_only | PASS | found 0 |
| V11 | keep_manual/reject 不进入 safe_only | PASS | found 0 |
| V12 | exclusion total >= 801 (582 + 219) | PASS | actual 801 |
| V13 | 原始注释保留（spot check 第一条 safe_only） | PASS | comment=ROW_ID |
| V14 | 未训练 Vanna（人工确认） | PASS |  |
| V15 | 未写入 vanna_data / agent_data（人工确认） | PASS |  |
| V16 | whitelist 注释逐行一致（与 columns_with_comments.csv 完全一致） | PASS | mismatch=0 |
| V17 | safe_candidate_only 注释逐行一致（与 columns_with_comments.csv 完全一致） | PASS | mismatch=0 |
| V18 | whitelist 字段均能回源 columns_with_comments.csv | PASS | missing_source=0 |
| V19 | safe_candidate_only 字段均能回源 columns_with_comments.csv | PASS | missing_source=0 |
| V20 | 原始注释未改写结论 | PASS | 原始注释逐字段完整性校验通过，未发现白名单改写原始注释。 |

## 结论

所有规则校验通过。清单修正符合要求。

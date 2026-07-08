# 剩余 A 档候选规则校验报告

**校验时间**: 2026-07-07

## 汇总

| 指标 | 数值 |
|------|------|
| 总规则数 | 15 |
| PASS | 15 |
| FAIL | 0 |

## 逐条结果

| 规则 | 说明 | 结果 | 详情 |
|------|------|------|------|
| R1 | review 总行数 = 5 | PASS | 实际 5 |
| R1b | decision 总行数 = 5 | PASS | 实际 5 |
| R2 | likely_approve = 1 | PASS | 实际 1 |
| R2b | keep_manual = 3 | PASS | 实际 3 |
| R2c | reject_candidate = 1 | PASS | 实际 1 |
| R3 | 所有 sample_support_level=none 均不是 likely_approve | PASS |  |
| R4 | 所有无样本值字段均不是 likely_approve | PASS |  |
| R5 | 所有 FK=False + sample=none 均不是 likely_approve | PASS |  |
| R6 | type_code 必须是 reject | PASS | 实际 reject_candidate |
| R7 | object_code 必须是 likely_approve | PASS | 实际 likely_approve_after_human_confirm |
| R8 | region_id 必须是 keep_manual | PASS | 实际 keep_manual |
| R9 | year 必须是 keep_manual | PASS | 实际 keep_manual |
| R10 | asset_id 必须是 keep_manual | PASS | 实际 keep_manual |
| R11 | 本脚本不检查 SQL 文件生成（由人工确认） | PASS |  |
| R12 | 本脚本未连接数据库（由人工确认） | PASS |  |

## 结论

✅ 所有规则校验通过。

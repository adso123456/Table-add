# Safe Candidate 人工审核分批计划

**生成时间**: 2026-07-08
**状态**: 只读生成，未训练 Vanna

---

## 1. 总字段数

safe_candidate_only 共 **1451** 条，涉及 **128** 张表。

---

## 2. 为什么要分批审核

1451 条字段一次审核工作量过大，且不同表的字段风险不同。
分批审核的好处：
- 优先处理高风险表（表注释缺失、字段数多）
- 每批控制在合理工作量范围内（建议每批 50–120 字段）
- 每批审核完成后可总结经验，优化后续批次的审核方法
- 发现问题可逐批修正，不影响已审核批次

---

## 3. 审核优先级分布

| 优先级 | 表数 | 说明 |
|--------|------|------|
| high | 1 | 表注释缺失，需优先审核 |
| medium | 14 | 有部分风险因素 |
| low | 113 | 表注释清楚且字段注释明确 |

---

## 4. 分批规划

共规划 **20** 批。

| 批次 | 名称 | 优先级 | 表数 | 字段数 | 状态 |
|------|------|--------|------|--------|------|
| batch_001 | 第1批：wm_raster_inversion 表（high priority） | high | 1 | 10 | ready_for_human_review |
| batch_002 | 第2批：medium priority 表（4张） | medium | 4 | 63 | planned_not_generated |
| batch_003 | 第3批：medium priority 表（1张） | medium | 1 | 54 | planned_not_generated |
| batch_004 | 第4批：medium priority 表（1张） | medium | 1 | 96 | planned_not_generated |
| batch_005 | 第5批：medium priority 表（2张） | medium | 2 | 95 | planned_not_generated |
| batch_006 | 第6批：medium priority 表（3张） | medium | 3 | 100 | planned_not_generated |
| batch_007 | 第7批：medium priority 表（3张） | medium | 3 | 59 | planned_not_generated |
| batch_008 | 第8批：low priority 表（10张） | low | 10 | 67 | planned_not_generated |
| batch_009 | 第9批：low priority 表（10张） | low | 10 | 28 | planned_not_generated |
| batch_010 | 第10批：low priority 表（10张） | low | 10 | 99 | planned_not_generated |
| batch_011 | 第11批：low priority 表（10张） | low | 10 | 74 | planned_not_generated |
| batch_012 | 第12批：low priority 表（10张） | low | 10 | 85 | planned_not_generated |
| batch_013 | 第13批：low priority 表（10张） | low | 10 | 82 | planned_not_generated |
| batch_014 | 第14批：low priority 表（8张） | low | 8 | 96 | planned_not_generated |
| batch_015 | 第15批：low priority 表（10张） | low | 10 | 71 | planned_not_generated |
| batch_016 | 第16批：low priority 表（10张） | low | 10 | 71 | planned_not_generated |
| batch_017 | 第17批：low priority 表（6张） | low | 6 | 84 | planned_not_generated |
| batch_018 | 第18批：low priority 表（8张） | low | 8 | 92 | planned_not_generated |
| batch_019 | 第19批：low priority 表（8张） | low | 8 | 92 | planned_not_generated |
| batch_020 | 第20批：low priority 表（3张） | low | 3 | 33 | planned_not_generated |

---

## 5. 第 1 批选择规则

batch_001 只包含 review_priority=high 的表：
- 涉及表: wm_raster_inversion
- 字段数: 10
- 如果超过 120 字段，按 suspicious 优先级排序取前 120
- 禁止把 medium / low 表放入 batch_001

---

## 6. 后续批次建议

1. batch_001 审核完成后，总结经验再启动 batch_002
2. 按 high → medium → low 顺序逐批推进
3. 每批审核前先了解涉及表的业务背景
4. **审核阶段仍不训练 Vanna**

---

## 7. 原始注释保护原则

- 所有 `column_comment` 来自 `columns_with_comments.csv` 原文
- 未做 strip / trim / normalize / 改写
- 审核过程中发现错误注释，标记为 `hold_for_business_review`，不直接修改
- 审核包中的注释与源文件完全一致

---

## 8. 禁止事项

1. 禁止自动填写 `approve_for_limited_training`
2. 禁止批量 approve
3. 禁止修改审核模板中的 column_comment
4. 禁止训练 Vanna
5. 禁止把 `hold_for_business_review` 的记录当成错误删除

---

## 9. 本阶段状态

**本阶段只生成第 1 批人工审核辅助包，不训练 Vanna，不写入 vanna_data / agent_data。**

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 总字段 1451, 128 张表 | 是 |
| 规划 20 批 | 是 |
| batch_001 =10 字段, 1 张表 | 是 |
| batch_001 只含 high 表 | 是 |
| 未训练 Vanna | 是 |
| 未写入 vanna_data / agent_data | 是 |


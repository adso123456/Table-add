# wm_raster_inversion 注释对齐候选 — 人工确认说明

**生成时间**: 2026-07-08
**状态**: 只读生成候选，未执行 SQL，未训练 Vanna

---

## 1. 为什么要补表级注释

`wm_raster_inversion` 当前无 table_comment，导致：

- 审核人员无法确认表的业务用途
- Text-to-SQL 模型训练时缺少关键的上下文信息
- 10 个字段全部命中 `missing_table_comment` 风险标记

补齐表级注释是后续所有工作的前提。

---

## 2. 为什么 record_id 当前注释疑似错误

| 现象 | 说明 |
|------|------|
| 当前注释 | `遥感反演结果表（合并版）` |
| 字段名 | `record_id` |
| 数据类型 | `bigint` |

该注释语义上描述的是整张表，而非 `record_id` 这个字段。
推测 DBA 在前序注释补齐流程中，误将表级描述填入了该表的第一个字段。
`record_id` 本身应是记录标识字段，建议修正为 `遥感反演结果记录ID`。

**但这条修正必须先经人工确认，不能自动执行。**

---

## 3. 为什么不能直接修改已有注释

原始注释保护原则要求：

1. 已有注释默认视为事实源
2. 修改已有注释 = 覆盖事实源，必须有人工确认的证据链
3. 不能因为'看起来像错误'就直接改——可能是我们理解有偏差
4. COMMENT ON COLUMN 是 DDL，执行后不可回退（除非有备份）
5. 本阶段只生成候选，人工确认后才进入 SQL 草案阶段

---

## 4. 为什么 service_url / data_time 不应编造更具体含义

| 字段 | 当前注释 | 为什么不编造 |
|------|----------|-------------|
| `service_url` | `服务地址` | 无法确认是 WMS/WFS/TMS/其他协议，编造含义反而引入错误 |
| `data_time` | `数据日期` | 无法确认是采集日期/处理日期/影像拍摄日期，编造含义反而引入错误 |

**原则**：不确定时不编造。等到有业务方确认的真实信息后再补充。

---

## 5. 其他字段（inversion_type、l1_area–l6_area）

这些字段的注释质量较高，包含明确的业务分类/枚举值，暂不提出修改候选。
它们的训练可用性取决于表级注释是否补齐。

---

## 6. 人工确认后才能进入 SQL 草案阶段

当前阶段不生成 SQL。人工确认后，后续阶段才会：

1. 生成 COMMENT ON TABLE / COMMENT ON COLUMN 草案
2. 通过人工执行检查清单确认
3. 由 DBA 在数据库执行

---

## 7. 本阶段状态

**本阶段不执行 SQL，不训练 Vanna，不写入 vanna_data / agent_data。**

---

## 人工确认步骤

1. 打开 `wm_raster_inversion_comment_alignment_candidate.csv`
2. 逐条审查候选注释是否合理
3. 在 `wm_raster_inversion_comment_alignment_decision_template.csv` 中填写 `human_decision`：
   - `approve`：确认候选注释正确
   - `hold_for_business_review`：不确定，需业务方/DBA 进一步确认
   - `reject`：候选注释不合理，应放弃
4. 不确定时填写 `hold_for_business_review`
5. 审批通过后才能进入 SQL 草案生成阶段

⚠️ **本阶段只是候选，不执行 SQL，不修改数据库，不训练 Vanna。**

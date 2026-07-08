# object_code 字段人工确认清单

**生成时间**: 2026-07-07
**来源**: remaining_a 候选审查（修正版）
**阶段**: 人工确认包，不生成 SQL

---

本阶段只生成确认包，不代表已经批准，不生成 SQL，不修改数据库。
所有证据必须来自 remaining_a 审查文件和样本文件，不得编造。

---

## 1. 表名

`wst_trace_topology_issue`

表无注释。上下文字段：`issue_type`（值：asset_unsnapped / empty_geometry / outlet_edge / snap_distance_too_far）、`object_type`、`object_id`、`object_name`。该表属于水安全溯源模块，用于记录拓扑质量问题。

---

## 2. 字段名

`object_code`

数据类型：`character varying`（varchar）

---

## 3. 建议注释

```text
监控对象编码
```

---

## 4. 证据摘要

| 维度 | 内容 |
|------|------|
| 证据表 | `stg_sslhhpj_hbsxkqycszhslzhglptjsxm_att_wmst_base_df` |
| 证据字段 | `object_code` (varchar) |
| 证据注释 | `监控对象编码` |
| 类型匹配 | ✅ 同为 varchar |
| 证据数量 | 1 个表 |
| 冲突检查 | comment_conflicts.csv 中无冲突 |

---

## 5. 样本值摘要

从 `wst_trace_topology_issue` 表查询 20 个 distinct 非空值，样本包含 3 种编码格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| FA-行政区划-序号-类型-状态 | FA-420582-0083-QT-00 | 完整设施编码 |
| rs_outlet_序号 | rs_outlet_947 | 排口编码 |
| HBYC日期序号 | HBYC2020111301 | 项目编码 |

全部 19 个 distinct 样本值均符合"监控对象编码"的编码格式特征。

---

## 6. 风险点

| # | 风险 | 说明 |
|---|------|------|
| 1 | **证据表只有 1 个，且来自 stg 前缀表，权威性中等，需要人工最终确认** | stg 表通常是数据接入的临时/接口表，其字段注释可能不权威 |
| 2 | 证据表与目标表前缀不同 | stg_sslhhpj vs wst_trace，非同一业务子模块 |
| 3 | 无显式外键 | 未在 pg_constraint 中发现 object_code 的外键约束 |

---

## 7. 不确定性

- 证据表 `stg_sslhhpj_...` 名称中包含 "wmst"（水安全溯源），与目标表 `wst_trace_topology_issue` 的 `wst` 前缀有语义关联，但并非直接同一子系统
- 仅 1 个证据表，不足以构成"跨表一致性"的强证据链
- 置信度评估：中等（有真实样本支撑但证据数量少）

---

## 8. 需要人工回答的问题

> **wst_trace_topology_issue 表的 object_code 字段是否表示"监控对象编码"？样本值（rs_outlet_*/FA-*/HBYC*）是否符合业务预期？**

---

## 9. 如果人工确认"是"

下一步：
1. 将 human_decision 填入 `object_code_confirm_decision_template.csv` 为 `approve`
2. 进入"人工确认 COMMENT ON COLUMN SQL 草案生成"阶段
3. 生成单条 `COMMENT ON COLUMN ... IS '监控对象编码'` SQL 草案
4. 经执行前最终确认后，受控执行

---

## 10. 如果人工确认"否"

下一步：
1. 将 human_decision 填入 `object_code_confirm_decision_template.csv` 为 `reject`
2. 该字段移出候选，标记为 keep_manual
3. 等待 DBA 或业务方提供正确注释后手工补注释

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 本阶段只生成确认包 | 是 |
| 未生成 SQL | 是 |
| 未修改数据库 | 是 |
| 未训练 Vanna | 是 |
| 证据全部来自 remaining_a 审查文件和样本文件 | 是 |
| 未编造样本值 | 是 |
| 未编造证据 | 是 |

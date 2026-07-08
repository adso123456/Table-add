# 剩余 5 条 A 档候选只读审查报告（修正版）

**审查时间**: 2026-07-07
**修正时间**: 2026-07-07
**阶段**: 只读审查，不补库
**修正原因**: 上一版中 3 个空表字段被错误升级为 likely_approve，违反"空表/无样本/无显式外键不得升级"规则

---

本阶段只做只读审查，不生成 SQL，不修改数据库，不训练 Vanna。
所有证据必须来自审计文件或只读数据库查询，不得编造。

---

## 修正说明

### 上一版错误

上一版 `remaining_a_review.csv` 中以下 3 条被错误标记为 `likely_approve_after_human_confirm`：

| 字段 | 问题 |
|------|------|
| gis_region_population.region_id | 表为空，sample_support_level=none，无显式外键 |
| gis_region_population.year | 表为空，sample_support_level=none，无显式外键 |
| wst_trace_node.asset_id | 表为空，sample_support_level=none，无显式外键 |

违反本阶段规则：

- 表为空或样本不足，必须 keep_manual
- 没有显式外键且关系不明确，必须 keep_manual
- 只能靠字段名推测，必须 keep_manual

### 已修正

3 条已全部改为 `keep_manual`。目前只有 `wst_trace_topology_issue.object_code`（有真实样本值，sample_support_level=high）可进入人工确认。`wm_raster_inversion_config.type_code` 继续保持 `reject_candidate`。

---

## 1. 本阶段读取的文件

| 文件 | 用途 |
|------|------|
| `comment_fill_candidates.csv` | 当前 5 条 A 档候选 |
| `columns_with_comments.csv` | 验证 has_comment=False |
| `tables_summary.csv` | 目标表概要信息 |
| `missing_comments.csv` | 验证字段仍在缺失列表 |
| `comment_conflicts.csv` | 检查是否有同名字段冲突 |
| `summary.md` | 审计报告概览 |

---

## 2. 是否连接数据库

**是。** 仅执行只读 SELECT 查询，用于样本取证和元数据验证。

---

## 3. 执行的只读 SELECT 类型

所有查询均使用 LIMIT，无 SELECT *，无 geom/geometry 字段查询。

---

## 4. 当前 A 档候选数量

**5 条**。

---

## 5. 逐条审查结果（修正后）

### #1 gis_region_population.region_id → "所属区域id" → keep_manual

**原因**: 表为空，sample_support_level=none，无显式外键。仅基于同名字段推断，不能作为自动补注释依据。待 DBA 确认。

### #2 gis_region_population.year → "年份" → keep_manual

**原因**: 表为空，sample_support_level=none，无显式外键。虽有 2 个证据表，但不满足自动升级条件。待 DBA 确认。

### #3 wm_raster_inversion_config.type_code → "关系大类编码..." → reject_candidate

**原因**: 目标 bigint vs 证据 varchar，类型不匹配。证据注释含文本示例值无法存入 bigint。业务域不相关。

### #4 wst_trace_node.asset_id → "资产ID，关联 wst_asset.id" → keep_manual

**原因**: 表为空，sample_support_level=none，无显式外键。同域证据质量虽高，但缺乏样本和外键支持。待 DBA 确认。

### #5 wst_trace_topology_issue.object_code → "监控对象编码" → likely_approve_after_human_confirm

**原因**: 有真实样本值（sample_support_level=high），样本值支持"监控对象编码"语义。同类型（varchar）。无冲突。但证据表仅 1 个（stg 前缀），仍需人工最终确认。

---

## 6. Recommendation 汇总（修正后）

| 决策 | 数量 | 字段 |
|------|------|------|
| `likely_approve_after_human_confirm` | **1** | wst_trace_topology_issue.object_code |
| `keep_manual` | **3** | gis_region_population.region_id, gis_region_population.year, wst_trace_node.asset_id |
| `reject_candidate` | **1** | wm_raster_inversion_config.type_code |

---

## 7. 是否发现编造风险或证据不足

**是。** 3 条空表字段无样本验证，已全部降为 keep_manual。

---

## 8. 是否生成 SQL

**否。** 本阶段只做只读审查，未生成任何 SQL。

---

## 9. 是否修改数据库

**否。** 所有数据库操作均为只读 SELECT。

---

## 10. 是否训练 Vanna

**否。**

---

## 11. 下一步建议（不要在本阶段执行）

1. **只能对 `wst_trace_topology_issue.object_code` 生成确认包**，不能处理其他 4 条
2. 3 条 keep_manual 等待 DBA 或业务方确认后手工补注释
3. 1 条 reject 移除候选列表
4. 不要训练 Vanna

---

## 自查清单

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 只处理 5 条 | ✅ |
| 2 | recommendation 分布为 1 / 3 / 1 | ✅ |
| 3 | sample_support_level=none 均不是 likely_approve | ✅ |
| 4 | 空表字段均不是 likely_approve | ✅ |
| 5 | 未生成 SQL | ✅ |
| 6 | 未修改数据库 | ✅ |
| 7 | 未训练 Vanna | ✅ |
| 8 | 未修改项目代码 | ✅ |
| 9 | 没有新增证据 | ✅ |
| 10 | 没有编造样本 | ✅ |

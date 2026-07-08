# batch_001 人工审核建议 V2 — 审核说明

**生成时间**: 2026-07-08
**版本**: V2（基于表注释补齐后）
**范围**: `batch_001` / `wm_raster_inversion` 表全部 10 个字段

---

## 一、V1 → V2 变化

| 维度 | V1（旧版） | V2（当前） |
|------|-----------|-----------|
| 表注释 `table_comment` | 空 | 遥感反演结果表（合并版） |
| record_id 字段注释 | 遥感反演结果表（合并版）（误填） | 遥感反演结果记录ID（已修正） |
| missing_table_comment 标记 | 存在（10 行） | 已清除 |
| 表级上下文 | 缺失 | 已知 |
| 审核基线 | 表注释缺失导致多处 hold | 表注释已补齐，可重新评估 |

---

## 二、各字段审核建议说明

### 2.1 record_id — `suggest_exclude_from_training`

- 已修正为字段级注释 `遥感反演结果记录ID`
- 但仍属通用 ID 类注释，对 Text-to-SQL 训练帮助有限
- 字段类型 bigint + 名含 `_id`，模型通常自行推断为主键/外键
- **建议**：排除训练

### 2.2 inversion_type — `suggest_possible_limited_training`

- 注释包含业务枚举值（水环境/水生态/土地利用），质量好
- code_like_field 风险仍存在，但注释有业务上下文
- 表注释已补齐，表级上下文已明确
- **建议**：有限训练

### 2.3 l1_area ~ l6_area（6 个字段） — `suggest_possible_limited_training`

- 注释包含明确的水质分类 + 面积指标，业务语义完整
- 表注释已补齐，原 `missing_table_comment` 风险已解除
- 这些字段是遥感反演的核心输出指标，对查询有直接价值
- **建议**：可纳入训练

### 2.4 service_url — `suggest_hold_for_business_review`

- 注释仅 `服务地址`，4 字，过于通用
- 无法区分是 WMS / WFS / 其他服务协议
- 表注释补齐后风险略有降低，但注释本身仍然模糊
- **建议**：业务确认后再定

### 2.5 data_time — `suggest_hold_for_business_review`

- 注释仅 `数据日期`，4 字，过于通用
- 无法区分是采集/处理/影像拍摄日期
- 表注释补齐后风险略有降低，但注释本身仍然模糊
- **建议**：业务确认后再定

---

## 三、与原 V1 建议对比

| 字段 | V1 建议 | V2 建议 | 变化原因 |
|------|---------|---------|----------|
| record_id | exclude_from_training | exclude_from_training | 不变（仍是 ID 类） |
| inversion_type | limited_training_after_table_context_confirmed | possible_limited_training | 表上下文已确认，建议升级 |
| l1_area~l6_area | limited_training_after_table_context_confirmed | possible_limited_training | 表上下文已确认，前提条件满足 |
| service_url | hold_for_business_review | hold_for_business_review | 不变（注释本身仍模糊） |
| data_time | hold_for_business_review | hold_for_business_review | 不变（注释本身仍模糊） |

---

## 四、风险解除声明

> 以下风险已在 V2 中解除：
>
> - ✅ `missing_table_comment`：表注释 `遥感反演结果表（合并版）` 已写入数据库并同步到衍生文件
> - ✅ record_id 注释误填：已从表级描述修正为字段级描述 `遥感反演结果记录ID`
>
> 以下风险仍然存在：
>
> - ⚠️ `id_like_field`：record_id 注释仍为通用 ID 描述
> - ⚠️ `very_short_comment`：service_url、data_time 注释仍过于简短
> - ⚠️ `time_like_field`：data_time 注释未明确时间语义

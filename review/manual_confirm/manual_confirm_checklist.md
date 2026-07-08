# needs_manual 人工确认清单

**生成时间**: 2026-07-07 16:12:04
**来源**: needs_manual_evidence.csv（3 条 likely_approve_after_human_confirm）
**状态**: 待人工确认，未批准

---

## 重要声明

本阶段只生成确认包，不代表已经批准，不生成 SQL，不修改数据库。
所有证据来自已有审计文件和样本文件，未编造任何证据。

---

## 纳入确认的 3 条字段

### 1. stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.cjsj

| 项目 | 内容 |
|------|------|
| **建议注释** | 创建时间 |
| **证据强度** | moderate |
| **样本支持度** | low |
| **风险等级** | low |

**证据摘要**：

- 同名字段已有一致注释：`创建时间`
- 证据表：见 `needs_manual_evidence.csv`
- 注释冲突：无
- 显式外键：未发现

**样本值摘要**：

   - `2022-04-14 11:38:46`

**风险点**：

cjsj 为拼音缩写；表仅含 1 行数据，样本量极低；同名字段证据来自同源 staging 表(stg_ycssthjj)，证据数仅 1；无法通过大量样本交叉验证；推测正确但需人工确认

**仍需人工确认的问题**：

> cjsj 在该 staging 表中是否确实代表'创建时间'？

**如人工确认为"是"**：

→ 可升级为 approved，参照已执行的 A 档 13 条流程生成 COMMENT ON SQL 并受控执行

**如人工确认为"否"**：

→ 保持 needs_manual，由业务方提供准确注释后手动补

---

### 2. stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.xgsj

| 项目 | 内容 |
|------|------|
| **建议注释** | 修改时间 |
| **证据强度** | moderate |
| **样本支持度** | low |
| **风险等级** | low |

**证据摘要**：

- 同名字段已有一致注释：`修改时间`
- 证据表：见 `needs_manual_evidence.csv`
- 注释冲突：无
- 显式外键：未发现

**样本值摘要**：

   - `2022-04-14 11:38:46`

**风险点**：

xgsj 为拼音缩写；表仅含 1 行数据，样本量极低；同名字段证据来自同源 staging 表(stg_ycssthjj)，证据数仅 1；无法通过大量样本交叉验证；推测正确但需人工确认

**仍需人工确认的问题**：

> xgsj 在该 staging 表中是否确实代表'修改时间'？

**如人工确认为"是"**：

→ 可升级为 approved，参照已执行的 A 档 13 条流程生成 COMMENT ON SQL 并受控执行

**如人工确认为"否"**：

→ 保持 needs_manual，由业务方提供准确注释后手动补

---

### 3. wm_waterbody_info.water_body_name

| 项目 | 内容 |
|------|------|
| **建议注释** | 水体名称 |
| **证据强度** | strong |
| **样本支持度** | high |
| **风险等级** | low |

**证据摘要**：

- 同名字段已有一致注释：`水体名称`
- 证据表：见 `needs_manual_evidence.csv`
- 注释冲突：无
- 显式外键：未发现

**样本值摘要**：

   - `官庄水库`
   - `香溪河`
   - `良斗河`
   - `运河`
   - `漳河`
   - `天池河`
   - `胡家畈水库`
   - `九畹溪`
   - `沮漳河`
   - `付家河水库`
   - ... (共 20 个)

**风险点**：

water_body_name 语义自明（字段名即含义）；20 个样本值全部为真实水库/河流名称，与'水体名称'高度吻合；证据表仅 1 张(wm_station_info_v2)，非同表族但同属 wm 域；不确定性低

**仍需人工确认的问题**：

> wm_waterbody_info 的 water_body_name 是否确实代表'水体名称'？(语义自明，确认即可)

**如人工确认为"是"**：

→ 可升级为 approved，参照已执行的 A 档 13 条流程生成 COMMENT ON SQL 并受控执行

**如人工确认为"否"**：

→ 保持 needs_manual，由业务方提供准确注释后手动补

---



## 排除说明

以下 3 条 `keep_manual` 字段不纳入本次确认：

| 字段 | 排除原因 |
|------|----------|
| gis_region_population.region_id | 表为空 + 跨业务域 + 证据不足 |
| gis_region_population.year | 表为空 + 跨业务域 + year 语义随表变化 |
| wst_trace_node.asset_id | 表为空 + 单证据 + 非通用审计字段 |

---

## 人工填写方式

使用 `manual_confirm_decision_template.csv`：

- `human_decision` 列填入 `approve` / `reject` / `keep_manual`
- `human_note` 列填入确认备注

---

⚠️ **本阶段只生成确认包，不代表已经批准，不生成 SQL，不修改数据库。所有证据必须来自已有审计文件和样本文件，不得编造。**

# needs_manual 6 字段只读证据增强报告

**生成时间**: 2026-07-07 16:05:39
**数据库**: gt_monitor (只读连接, readonly=True)

---

## 读取文件

| 文件 | 用途 |
|------|------|
| a_candidates_needs_manual.csv | 6 条待确认字段 |
| columns_with_comments.csv | 同名字段注释查询 |
| tables_summary.csv | 表注释查询 |
| comment_conflicts.csv | 冲突检测 |
| summary.md | 当前审计状态 |

---

## 数据库只读查询

| 查询类型 | 限制 |
|----------|------|
| information_schema.columns | 目标字段 + 上下文字段 |
| pg_constraint / information_schema FK | 外键关系 |
| SELECT DISTINCT 样本值 | LIMIT 20, 非空 |
| SELECT count(*) 非空估算 | 全表 count |
| 查询表数 | 6 (仅目标表) |
| SELECT * | 否 |
| geom/geometry 查询 | 否 |
| 全表扫描 | 否 (DISTINCT + LIMIT 20) |

---

## 建议汇总

| 建议 | 数量 |
|------|------|
| likely_approve_after_human_confirm | **3** |
| keep_manual | **3** |
| reject_candidate | **0** |
| **合计** | **6** |

---

## 逐条证据详情

### gis_region_population.region_id

| 项目 | 内容 |
|------|------|
| 目标表注释 | (空缺) |
| 字段类型 | bigint |
| proposed_comment | 所属区域id |
| 同名字段已有注释 | 所属区域id |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | none |
| 证据强度 | moderate |
| 建议 | **keep_manual** |
| 理由 | 证据表数量不足; 需人工确认后决定 |

### gis_region_population.year

| 项目 | 内容 |
|------|------|
| 目标表注释 | (空缺) |
| 字段类型 | bigint |
| proposed_comment | 年份 |
| 同名字段已有注释 | 年份 |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | none |
| 证据强度 | moderate |
| 建议 | **keep_manual** |
| 理由 | 需人工确认后决定 |

### stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.cjsj

| 项目 | 内容 |
|------|------|
| 目标表注释 | 监控数据_日数据_污染物_ |
| 字段类型 | timestamp without time zone |
| proposed_comment | 创建时间 |
| 同名字段已有注释 | 创建时间 |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | low |
| 证据强度 | moderate |
| 建议 | **likely_approve_after_human_confirm** |
| 理由 | 同名字段有一致注释(1种); 人工确认后可批准 |

### stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df.xgsj

| 项目 | 内容 |
|------|------|
| 目标表注释 | 监控数据_日数据_污染物_ |
| 字段类型 | timestamp without time zone |
| proposed_comment | 修改时间 |
| 同名字段已有注释 | 修改时间 |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | low |
| 证据强度 | moderate |
| 建议 | **likely_approve_after_human_confirm** |
| 理由 | 同名字段有一致注释(1种); 人工确认后可批准 |

### wm_waterbody_info.water_body_name

| 项目 | 内容 |
|------|------|
| 目标表注释 | 水体信息实体类 |
| 字段类型 | character varying |
| proposed_comment | 水体名称 |
| 同名字段已有注释 | 水体名称 |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | high |
| 证据强度 | strong |
| 建议 | **likely_approve_after_human_confirm** |
| 理由 | 样本值支持(20 distinct values); 同名字段有一致注释(1种); 人工确认后可批准 |

### wst_trace_node.asset_id

| 项目 | 内容 |
|------|------|
| 目标表注释 | 水安全溯源模块-溯源拓扑节点表，用于存储河网、管网、园区排污河流、排口挂接点、断面挂接点、园区出口等 pgRouting 节点 |
| 字段类型 | bigint |
| proposed_comment | 资产ID，关联 wst_asset.id |
| 同名字段已有注释 | 资产ID，关联 wst_asset.id |
| 注释冲突 | 否 |
| 外键 | 未发现显式外键 |
| 样本支持度 | none |
| 证据强度 | moderate |
| 建议 | **keep_manual** |
| 理由 | 证据表数量不足; 需人工确认后决定 |



---

## 关键发现

1. **外键证据**: 0 条字段发现显式外键
2. **样本支持**: 1 条 high, 0 条 medium, 2 条 low
3. **注释冲突**: 0 条字段的同名字段存在注释冲突
4. **数据库已连接**: 是 (只读, autocommit, readonly=True)
5. **数据库已修改**: 否
6. **SQL 已生成**: 否
7. **Vanna 已训练**: 否

---

## 下一步建议

1. **likely_approve 的 3 条**: 人工确认后可按 A 档流程生成 COMMENT ON SQL 并受控执行
2. **keep_manual 的 3 条**: 需要 DBA 或业务方确认字段含义后手动补注释
3. 建议先处理 likely_approve 字段，再集中精力处理 keep_manual
4. 本阶段不执行补注释，不训练 Vanna

---

⚠️ 本阶段仅做只读证据增强，未修改数据库，未生成 SQL，未训练 Vanna。

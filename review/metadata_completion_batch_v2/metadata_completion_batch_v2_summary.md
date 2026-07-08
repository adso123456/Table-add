# 全库缺注释候选生成 V2 — 汇总报告

**生成时间**: 2026-07-08
**状态**: 候选已生成，未执行 COMMENT ON，未训练 Vanna

---

## 一、扫描范围

| 项目 | 值 |
|------|-----|
| Schema | public |
| 数据库 | gt_monitor (local-timescale) |
| 总表数（含已有注释表） | public schema 所有普通表 |

---

## 二、扫描结果

| 指标 | 数量 |
|------|------|
| 缺字段注释 | 582 |
| 缺表注释 | 18 |

---

## 三、分级统计

| 分级 | 说明 | 字段数 | 表数 |
|------|------|--------|------|
| A_auto_safe | 高置信度，可批量补 | 299 | 13 |
| B_review | 有候选，需人工快速确认 | 262 | 0 |
| C_hold | 证据不足，暂缓 | 21 | 5 |
| **合计** | | **582** | **18** |

---

## 四、A_auto_safe 候选说明

主要来源：

1. **标准审计字段**：create_by / create_time / update_by / update_time / del_flag — 跨所有表
2. **标准 ID 字段**：id / gid / objectid / region_id 等
3. **几何字段**：geom
4. **通用高频字段**：name / code / type / address / remark 等
5. **表域规则高置信**：如 gis_ecologicalregion 的表名语义确定性很高

---

## 五、B_review 候选说明

需要人工确认的场景：

1. **气象预测字段**：基于字段名缩写推断物理量含义，需气象业务方确认
2. **特定业务字段**：如自然保护区特有字段、水源地特有字段等，注释基于表名语义推断
3. **临时导入表**：基于原始字段名推断，业务方确认后可直接升级为 A
4. **JSON / JSONB 字段**：推断可能包含的内容类型

---

## 六、C_hold 候选说明

暂缓的场景：

1. **系统表**（如 spatial_ref_sys — PostGIS 内置表）
2. **备份表**（_bak 后缀，注释应与主表同步）
3. **临时表**（_stg 前缀，字段名简写难以推断）
4. **年份命名字段**（如 2021, 2025, 2035）
5. **信息严重不足**的字段

---

## 七、生成文件清单

| 文件 | 内容 |
|------|------|
| `missing_comment_candidates_v2.csv` | 全量缺字段注释候选（582 行） |
| `missing_table_comment_candidates_v2.csv` | 全量缺表注释候选（18 行） |
| `auto_safe_candidates_v2.csv` | A_auto_safe 候选（312 行） |
| `review_needed_candidates_v2.csv` | B_review 候选（262 行） |
| `hold_candidates_v2.csv` | C_hold 候选（26 行） |
| `metadata_completion_batch_v2_summary.md` | 本汇总报告 |
| `generate_metadata_completion_candidates_v2.py` | 生成脚本 |

---

## 八、阶段边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改已有注释
> - ❌ 未修改项目代码

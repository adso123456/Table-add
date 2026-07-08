# wm_raster_inversion 刷新后完整性校验报告

**校验时间**: 2026-07-08
**状态**: 只读校验完成，未训练 Vanna

---

## 一、record_id 注释校验

| 文件 | 行号 | 实际值 | 预期值 | 结果 |
|------|------|--------|--------|------|
| `columns_with_comments.csv` | 2516 | 遥感反演结果记录ID | 遥感反演结果记录ID | ✅ |
| `vanna_training_safe_candidate_only.csv` | 1083 | 遥感反演结果记录ID | 遥感反演结果记录ID | ✅ |
| `batch_001_review_template.csv` | 2 | 遥感反演结果记录ID | 遥感反演结果记录ID | ✅ |

---

## 二、table_comment 校验

### safe_candidate_only.csv（10 行全量）

| 行号 | 字段 | table_comment | 结果 |
|------|------|---------------|------|
| 1083 | record_id | 遥感反演结果表（合并版） | ✅ |
| 1084 | inversion_type | 遥感反演结果表（合并版） | ✅ |
| 1085 | l1_area | 遥感反演结果表（合并版） | ✅ |
| 1086 | l2_area | 遥感反演结果表（合并版） | ✅ |
| 1087 | l3_area | 遥感反演结果表（合并版） | ✅ |
| 1088 | l4_area | 遥感反演结果表（合并版） | ✅ |
| 1089 | l5_area | 遥感反演结果表（合并版） | ✅ |
| 1090 | l6_area | 遥感反演结果表（合并版） | ✅ |
| 1091 | service_url | 遥感反演结果表（合并版） | ✅ |
| 1092 | data_time | 遥感反演结果表（合并版） | ✅ |

### batch_001_review_template.csv（10 行全量）

| 行号 | 字段 | table_comment | 结果 |
|------|------|---------------|------|
| 2 | record_id | 遥感反演结果表（合并版） | ✅ |
| 3 | inversion_type | 遥感反演结果表（合并版） | ✅ |
| 4 | l1_area | 遥感反演结果表（合并版） | ✅ |
| 5 | l2_area | 遥感反演结果表（合并版） | ✅ |
| 6 | l3_area | 遥感反演结果表（合并版） | ✅ |
| 7 | l4_area | 遥感反演结果表（合并版） | ✅ |
| 8 | l5_area | 遥感反演结果表（合并版） | ✅ |
| 9 | l6_area | 遥感反演结果表（合并版） | ✅ |
| 10 | service_url | 遥感反演结果表（合并版） | ✅ |
| 11 | data_time | 遥感反演结果表（合并版） | ✅ |

---

## 三、missing_table_comment 校验

| 文件 | 搜索 `missing_table_comment` | 结果 |
|------|------------------------------|------|
| `batch_001_review_template.csv` | 未找到 | ✅ 已全部清除 |

---

## 四、误改检查

| 检查项 | 方法 | 结果 |
|--------|------|------|
| 是否只影响 wm_raster_inversion | `grep wm_raster_inversion` 仅命中该表 | ✅ |
| 旧 record_id 注释是否残留 | `grep "遥感反演结果表（合并版）"` 仅在 table_comment 列出现 | ✅ |
| 其他字段注释未变 | 抽查 inversion_type, l1_area 等无变化 | ✅ |

---

## 五、校验结论

| 校验项 | 结论 |
|--------|------|
| record_id 注释全部正确 | ✅ |
| table_comment 全部正确（20 行） | ✅ |
| missing_table_comment 已清除 | ✅ |
| 误改 | ❌ 无 |
| 训练 Vanna | ❌ 未训练 |

---

## 六、阶段边界声明

> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库
> - ❌ 未执行 SQL
> - ❌ 未修改 CSV
> - ❌ 未修改项目代码

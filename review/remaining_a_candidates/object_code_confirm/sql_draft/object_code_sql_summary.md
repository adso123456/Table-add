# object_code COMMENT ON COLUMN SQL 草案报告

**生成时间**: 2026-07-07
**来源**: object_code_confirm_decision_template.csv
**阶段**: SQL 草案生成，不执行

---

本阶段未连接数据库，未执行 SQL，未修改数据库，未训练 Vanna。

---

## 读取文件

| 文件 | 用途 |
|------|------|
| object_code_confirm_decision_template.csv | 人工确认结果（1 approve） |
| columns_with_comments.csv | 确认字段当前无注释 |
| tables_summary.csv | 确认表存在于主表集合 |

---

## 统计

| 指标 | 数值 |
|------|------|
| 人工确认 approve 总数 | **1** |
| 生成 SQL 条数 | **1** |
| skipped 数量 | 0 |

---

## 生成 SQL 清单

| 字段 | 注释 | 人工备注 |
|------|------|----------|
| wst_trace_topology_issue.object_code | 监控对象编码 | 人工确认：object_code 表示监控对象编码；样本 rs_outlet_*/FA-*/HBYC* 符合业务预期 |

---

## skipped 明细

无。唯一 approve 字段已成功生成。

---

## 合规检查

| 检查项 | 结果 |
|------|------|
| 只包含 object_code | 是 |
| 不包含 keep_manual 字段 | 是 |
| 不包含 reject_candidate 字段 | 是 |
| 不包含 B 档字段 | 是 |
| 不包含 C 档字段 | 是 |
| 不包含其他 missing 字段 | 是 |
| 不包含 UPDATE / DELETE / INSERT / DROP / ALTER / CREATE | 是 |
| 不包含 BEGIN / COMMIT | 是 |
| 未连接数据库 | 是 |
| 未执行 SQL | 是 |
| 未修改数据库 | 是 |
| 未训练 Vanna | 是 |

---

## SQL 草案文件

- SQL: `review/remaining_a_candidates/object_code_confirm/sql_draft/object_code_comment_on_column_draft.sql`
- Manifest: `review/remaining_a_candidates/object_code_confirm/sql_draft/object_code_comment_manifest.csv`

---

## 下一步建议

进入执行前最终确认阶段，确认后按与之前相同的 Docker 方式受控执行。不要在本阶段执行。

---

本阶段未连接数据库，未执行 SQL，未修改数据库，未训练 Vanna。

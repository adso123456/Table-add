# object_code 单条 COMMENT ON COLUMN 执行命令草案

**生成时间**: 2026-07-07
**来源**: 执行前最终确认清单 (object_code_pre_execution_checklist.md)

---

本文件只提供命令草案，本阶段未执行任何命令。

---

## 待执行 SQL

共 **1** 条 COMMENT ON COLUMN：

```sql
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_code" IS '监控对象编码';
```

---

## 执行方式一：Docker 容器方式

```powershell
Get-Content "E:\3\code\metadata_audit\review\remaining_a_candidates\object_code_confirm\sql_draft\object_code_comment_on_column_draft.sql" | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

预期输出：1 行 `COMMENT` 确认信息，无错误。

---

## 执行方式二：本地 psql 方式

```powershell
psql "postgresql://postgres:test123456@localhost:5433/gt_monitor" -f "E:\3\code\metadata_audit\review\remaining_a_candidates\object_code_confirm\sql_draft\object_code_comment_on_column_draft.sql"
```

预期输出：1 行 `COMMENT` 确认信息，无错误。

---

## 执行后验证：重新审计

```powershell
& "E:\3\posgresql\1\vanna_venv\Scripts\python.exe" "E:\3\code\metadata_audit\run_metadata_audit.py"
```

---

## 执行后预期变化

| 指标 | 执行前 | 执行后（预期） |
|------|--------|---------------|
| 有字段注释字段数 | 2862 | 2863 |
| 缺字段注释字段数 | 583 | 582 |
| A 档候选 | 5 | 4 或 object_code 从候选中消失 |
| object_code 在 missing_comments.csv | 存在 | 消失 |
| object_code 在 comment_fill_candidates.csv | 存在 | 消失 |
| object_code 在 columns_with_comments.csv has_comment | False | True |

注意：精确数值以重新审计结果为准。

---

## 注意事项

1. 此 COMMENT 来自人工确认（approve），不是 AI 自动生成
2. 执行前确认目标数据库为 `gt_monitor`，端口 `5433`
3. 执行前确认 Docker 容器 `local-timescale` 正在运行
4. COMMENT ON COLUMN 是纯元数据操作，不修改表数据，无锁表风险
5. 如需回滚，执行 `COMMENT ON COLUMN ... IS NULL` 即可清除注释

---

## 回滚方式

```sql
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_code" IS NULL;
```

执行方式：

```powershell
# Docker 方式回滚
echo 'COMMENT ON COLUMN public."wst_trace_topology_issue"."object_code" IS NULL;' | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

---

本文件只提供命令草案，本阶段未执行任何命令。

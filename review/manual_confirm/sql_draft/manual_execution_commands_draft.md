# 人工确认 COMMENT ON COLUMN 执行命令草案

**生成时间**: 2026-07-07
**来源**: 执行前最终确认清单 (manual_pre_execution_checklist.md)

---

本文件只提供命令草案，本阶段未执行任何命令。

---

## 待执行 SQL

共 **3** 条 COMMENT ON COLUMN：

```sql
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."cjsj" IS '创建时间';
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."xgsj" IS '修改时间';
COMMENT ON COLUMN public."wm_waterbody_info"."water_body_name" IS '水体名称';
```

---

## 执行方式一：Docker 容器方式

```powershell
Get-Content "E:\3\code\metadata_audit\review\manual_confirm\sql_draft\manual_confirm_comment_on_columns_draft.sql" | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

预期输出：3 行 `COMMENT` 确认信息，无错误。

---

## 执行方式二：本地 psql 方式

```powershell
psql "postgresql://postgres:test123456@localhost:5433/gt_monitor" -f "E:\3\code\metadata_audit\review\manual_confirm\sql_draft\manual_confirm_comment_on_columns_draft.sql"
```

预期输出：3 行 `COMMENT` 确认信息，无错误。

---

## 执行后验证：重新审计

```powershell
& "E:\3\posgresql\1\vanna_venv\Scripts\python.exe" "E:\3\code\metadata_audit\run_metadata_audit.py"
```

---

## 执行后预期变化

| 指标 | 执行前 | 执行后（预期） |
|------|--------|---------------|
| 有字段注释字段数 | 2859 | 2862 |
| 缺字段注释字段数 | 586 | 583 |
| 字段注释覆盖率 | ~83.0% | ~83.1% |
| A 档候选 | 8 | 可能继续下降 |
| 3 个字段是否从 missing_comments.csv 消失 | — | 是 |

注意：覆盖率精确值以重新审计结果为准。

---

## 注意事项

1. 这 3 条 COMMENT 来自人工确认（approve），不是 AI 自动生成
2. 执行前确认目标数据库为 `gt_monitor`，端口 `5433`
3. 执行前确认 Docker 容器 `local-timescale` 正在运行
4. COMMENT ON COLUMN 是纯元数据操作，不修改表数据，无锁表风险
5. 如需回滚，执行 `COMMENT ON COLUMN ... IS NULL` 即可清除注释（见下方回滚方式）

---

## 回滚方式

如执行后发现注释有误，可用以下 SQL 清除：

```sql
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."cjsj" IS NULL;
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."xgsj" IS NULL;
COMMENT ON COLUMN public."wm_waterbody_info"."water_body_name" IS NULL;
```

执行方式：

```powershell
# Docker 方式回滚
@"
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."cjsj" IS NULL;
COMMENT ON COLUMN public."stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df"."xgsj" IS NULL;
COMMENT ON COLUMN public."wm_waterbody_info"."water_body_name" IS NULL;
"@ | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

---

本文件只提供命令草案，本阶段未执行任何命令。

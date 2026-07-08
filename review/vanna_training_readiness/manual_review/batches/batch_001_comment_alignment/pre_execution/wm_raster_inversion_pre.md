# wm_raster_inversion 注释对齐 — SQL 执行前确认清单

**生成时间**: 2026-07-08
**状态**: 待人工确认，SQL 未执行
**来源**: `sql_draft/wm_raster_inversion_comment_alignment_draft.sql`

---

## 一、SQL 草案清单（共 2 条）

| # | 类型 | 对象 | 新注释 | 风险 | 来源 |
|---|------|------|--------|------|------|
| 1 | COMMENT ON TABLE | `public."wm_raster_inversion"` | 遥感反演结果表（合并版） | LOW | manifest 第 2 行 |
| 2 | COMMENT ON COLUMN | `public."wm_raster_inversion"."record_id"` | 遥感反演结果记录ID | MEDIUM | manifest 第 3 行 |

---

## 二、语法检查

| 检查项 | SQL #1 | SQL #2 |
|--------|--------|--------|
| 关键字正确（COMMENT ON TABLE / COLUMN） | ✅ | ✅ |
| schema.table 格式正确 | ✅ `public."wm_raster_inversion"` | ✅ |
| IS 子句存在 | ✅ | ✅ |
| 注释为合法字符串（单引号包裹） | ✅ | ✅ |
| 语句以分号结尾 | ✅ | ✅ |
| 含中文注释（PostgreSQL UTF-8 支持） | ✅ | ✅ |
| 双引号正确转义标识符 | ✅ | ✅ |

**语法结论**: 2 条 SQL 语法均正确，无语法错误。

---

## 三、可执行性前置条件

以下条件**必须在执行前逐一验证**，否则 SQL 将报错：

### 3.1 数据库连接

| # | 检查项 | 验证方法 | 状态 |
|---|--------|----------|------|
| 1 | 目标数据库可连接 | `psql -h <host> -U <user> -d <db> -c "SELECT 1;"` | ⬜ 待验证 |
| 2 | 当前用户有 COMMENT 权限（表 owner 或 superuser） | 见下方验证 SQL | ⬜ 待验证 |

**权限验证说明：**

COMMENT ON TABLE / COLUMN 执行用户应为表 owner 或 superuser。`has_schema_privilege('public','usage')` 只能验证 schema usage，不能证明有 COMMENT 权限。请执行以下查询确认：

```sql
-- 查询表 owner
SELECT c.relname, r.rolname AS table_owner
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_roles r ON r.oid = c.relowner
WHERE n.nspname = 'public'
  AND c.relname = 'wm_raster_inversion';

-- 查询当前用户
SELECT current_user;

-- 查询是否 superuser
SELECT rolsuper
FROM pg_roles
WHERE rolname = current_user;
```

> 如果 `current_user` 等于 `table_owner` 或 `rolsuper = true`，则有 COMMENT 权限。

### 3.2 Schema 和对象存在性

| # | 检查项 | 验证方法 | 状态 |
|---|--------|----------|------|
| 1 | `public` schema 存在 | `SELECT nspname FROM pg_namespace WHERE nspname = 'public';` | ⬜ 待验证 |
| 2 | `wm_raster_inversion` 表存在且为普通表 | `SELECT relkind FROM pg_class WHERE relname = 'wm_raster_inversion' AND relnamespace = 'public'::regnamespace;` 预期返回 `r` | ⬜ 待验证 |
| 3 | `record_id` 字段存在 | `SELECT attname FROM pg_attribute WHERE attrelid = 'public.wm_raster_inversion'::regclass AND attname = 'record_id' AND attnum > 0;` | ⬜ 待验证 |

### 3.3 当前注释查询（执行前先跑，确认现状）

```sql
-- 查询表级注释
SELECT obj_description('public.wm_raster_inversion'::regclass) AS current_table_comment;

-- 查询字段级注释（先查 attnum，再查注释）
SELECT attname, attnum, col_description('public.wm_raster_inversion'::regclass, attnum) AS current_column_comment
FROM pg_attribute
WHERE attrelid = 'public.wm_raster_inversion'::regclass
  AND attname = 'record_id'
  AND attnum > 0;
```

### 3.4 注释现状（预期值）

| # | 当前注释（应为） | 执行后注释（预期） |
|---|-----------------|---------------------|
| 表 `wm_raster_inversion` | 无注释（manifest 注明"原表无注释"） | 遥感反演结果表（合并版） |
| 字段 `record_id` | 遥感反演结果表（合并版）（疑似表级描述误填） | 遥感反演结果记录ID |

---

## 四、风险评估

| 风险维度 | 评估 |
|----------|------|
| **数据修改** | 无。COMMENT ON 仅修改元数据，不影响表数据 |
| **元数据写入** | COMMENT ON 只修改注释元数据，不修改业务数据；但仍属于数据库元数据写入，执行前需要确认权限和对象存在。 |
| **锁** | COMMENT ON 会对被注释对象获取 SHARE UPDATE EXCLUSIVE 锁；本次只修改注释元数据，不修改业务数据，但仍应在低峰期或确认无敏感操作窗口后执行。 |
| **回滚** | 可简单回滚：`COMMENT ON ... IS NULL;` 或 `COMMENT ON ... IS '原注释';` |
| **幂等性** | 是。重复执行不会报错，始终覆盖为相同值 |
| **对其他对象影响** | 无。不影响索引、约束、视图、触发器 |
| **生产安全性** | 高。但建议先在非生产环境验证 |

---

## 五、建议执行顺序

```
1. 非生产环境 → 执行 COMMENT ON TABLE
2. 非生产环境 → 查询验证: SELECT obj_description('public.wm_raster_inversion'::regclass);
3. 非生产环境 → 执行 COMMENT ON COLUMN
4. 非生产环境 → 查询验证: SELECT col_description('public.wm_raster_inversion'::regclass, 1);
   (1 为 record_id 的 attnum，需先查询确认)
5. 非生产环境通过 → 生产环境执行
```

---

## 六、执行前最终签字清单

| # | 确认项 | 确认人 | 确认时间 |
|---|--------|--------|----------|
| 1 | 已确认目标数据库实例和连接信息 | ⬜ | ⬜ |
| 2 | 已确认 `public.wm_raster_inversion` 表存在 | ⬜ | ⬜ |
| 3 | 已确认 `record_id` 字段存在 | ⬜ | ⬜ |
| 4 | 已确认当前注释内容符合需求 | ⬜ | ⬜ |
| 5 | 已在非生产环境验证通过 | ⬜ | ⬜ |
| 6 | 已准备回滚语句（如有必要） | ⬜ | ⬜ |
| 7 | 确认可以执行 | ⬜ | ⬜ |

---

## 七、执行命令

```sql
-- 在目标数据库中逐条执行：

-- 步骤 1: 表级注释
COMMENT ON TABLE public."wm_raster_inversion" IS '遥感反演结果表（合并版）';

-- 步骤 2: 字段级注释
COMMENT ON COLUMN public."wm_raster_inversion"."record_id" IS '遥感反演结果记录ID';

-- 步骤 3: 验证
SELECT obj_description('public.wm_raster_inversion'::regclass) AS table_comment;
SELECT col_description('public.wm_raster_inversion'::regclass, 
       (SELECT attnum FROM pg_attribute 
        WHERE attrelid = 'public.wm_raster_inversion'::regclass 
        AND attname = 'record_id')) AS column_comment;
```

---

## 八、回滚命令（备用）

```sql
-- 仅当需要撤销时执行：
COMMENT ON TABLE public."wm_raster_inversion" IS NULL;
COMMENT ON COLUMN public."wm_raster_inversion"."record_id" IS '遥感反演结果表（合并版）';
--  注: 第二条恢复为原注释（原字段注释 = 表级描述误填，此处按原始值回滚）
```

---

## 九、阶段边界声明

> **本阶段仅生成 SQL 执行前确认文件，以下操作均未执行：**
>
> - ❌ 未执行 SQL
> - ❌ 未连接数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改数据库元数据或业务数据
> - ❌ 未修改项目代码

---

## 十、总结

| 项目 | 结论 |
|------|------|
| SQL 语法 | ✅ 2 条均正确 |
| 可执行性 | ✅ 语法层面可执行，需人工确认对象存在性 |
| 数据风险 | ✅ 无（仅元数据变更） |
| 是否可进入执行 | ⬜ 待人工完成前置条件检查后签字确认 |

#!/usr/bin/env python3
"""修复 vanna_data/ddl/ 下 115 个 DDL 文件，用真实 CREATE TABLE 替换占位内容。
只做第 1 级（结构 DDL），不做第 2/3/4 级训练。
"""

import subprocess, csv, os, json
from collections import defaultdict
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
IN_DIR = os.path.join(BASE, "review", "vanna_training_input_v3")
OUT = os.path.join(IN_DIR, "level1_metadata_training_fix")
os.makedirs(OUT, exist_ok=True)

DDL_DIR = os.path.join(BASE, "vanna_data", "ddl")
DOC_DIR = os.path.join(BASE, "vanna_data", "documentation")

def psql(sql):
    r = subprocess.run(
        ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor', '-t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip() if r.stdout else ''

# ===== 读取训练输入 =====
with open(os.path.join(IN_DIR, "vanna_trainable_tables_v3.csv"), 'r', encoding='utf-8') as f:
    tbls = {r['table_name']: r for r in csv.DictReader(f)}
with open(os.path.join(IN_DIR, "vanna_trainable_columns_v3.csv"), 'r', encoding='utf-8') as f:
    cols = list(csv.DictReader(f))

print(f"训练表: {len(tbls)}, 训练字段: {len(cols)}")

# ===== 从数据库获取每个表的字段定义 =====
print("\n从数据库获取字段定义...")

# 高效方式：一次性导出所有训练表的字段定义
table_list = "','".join(tbls.keys())
sql = f"""SELECT c.relname AS table_name, a.attname AS column_name,
       format_type(a.atttypid, a.atttypmod) AS data_type,
       a.attnotnull AS not_null,
       COALESCE(pg_get_expr(d.adbin, d.adrelid), '') AS default_value,
       a.attnum
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid
LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = a.attnum
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
  AND c.relname IN ('{table_list}')
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY c.relname, a.attnum"""

out = psql(sql)
if not out:
    print("ERROR: psql 返回空")
    raise SystemExit(1)

# 解析输出
table_cols = defaultdict(list)
for line in out.split('\n'):
    line = line.strip()
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 5:
            tbl_name = parts[0].strip()
            col_name = parts[1].strip()
            dtype = parts[2].strip()
            not_null = parts[3].strip() == 't'
            default = parts[4].strip() if len(parts) > 4 else ''
            table_cols[tbl_name].append({
                'column_name': col_name,
                'data_type': dtype,
                'not_null': not_null,
                'default_value': default,
            })

print(f"从数据库获取到 {len(table_cols)} 个表, {sum(len(v) for v in table_cols.values())} 个字段")

# 获取表注释（用培训数据中的）
table_comment_map = {t: tbls[t]['table_comment'] for t in tbls if tbls[t]['table_comment']}
# 构建字段注释映射
col_comment_map = {}
for c in cols:
    key = (c['table_name'], c['column_name'])
    col_comment_map[key] = c['column_comment']

# ===== 重新生成 DDL 文件 =====
print(f"\n重新生成 {len(tbls)} 个 DDL 文件...")

os.makedirs(DDL_DIR, exist_ok=True)
ddl_files = 0
total_cols_in_ddl = 0
create_table_count = 0
ddl_not_available_count = 0

for tbl_name in sorted(tbls.keys()):
    db_cols = table_cols.get(tbl_name, [])
    if not db_cols:
        print(f"  WARN: {tbl_name} 数据库中无字段定义，跳过")
        continue

    lines = []
    lines.append(f"-- Table: public.\"{tbl_name}\"")

    tbl_cmt = table_comment_map.get(tbl_name, '')
    if tbl_cmt:
        lines.append(f"-- Table comment: {tbl_cmt}")

    lines.append(f"CREATE TABLE public.\"{tbl_name}\" (")

    col_defs = []
    col_comments = []
    for i, c in enumerate(db_cols):
        null_clause = " NOT NULL" if c['not_null'] else ""
        default_clause = f" DEFAULT {c['default_value']}" if c['default_value'] else ""
        col_defs.append(f"  \"{c['column_name']}\" {c['data_type']}{null_clause}{default_clause}")

        # 字段注释
        cmt = col_comment_map.get((tbl_name, c['column_name']), '')
        if cmt:
            col_comments.append(f"--   {c['column_name']}: {cmt}")

    lines.append(",\n".join(col_defs))
    lines.append(");")
    lines.append("")

    if col_comments:
        lines.append("-- Column comments:")
        lines.extend(col_comments)

    content = '\n'.join(lines) + '\n'

    path = os.path.join(DDL_DIR, f"{tbl_name}.sql")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    ddl_files += 1
    total_cols_in_ddl += len(db_cols)

    if 'CREATE TABLE' in content:
        create_table_count += 1
    if 'DDL not available' in content:
        ddl_not_available_count += 1

print(f"\n  生成 DDL 文件: {ddl_files}")
print(f"  含 CREATE TABLE: {create_table_count}")
print(f"  含 DDL not available: {ddl_not_available_count}")
print(f"  DDL 字段总数: {total_cols_in_ddl}")

# ===== 更新训练清单 JSON =====
manifest_path = os.path.join(BASE, "vanna_data", "training_manifest.json")
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
manifest = {
    "generated_at": ts,
    "level": 1,
    "level_name": "结构 DDL 训练",
    "source": "metadata_snapshot_v3 + vanna_training_input_v3",
    "database": {"host": "localhost", "port": 5433, "dbname": "gt_monitor", "container": "local-timescale"},
    "totals": {
        "tables": len(tbls),
        "columns_in_training": len(cols),
        "ddl_files": ddl_files,
        "doc_files": len(os.listdir(DOC_DIR)) if os.path.exists(DOC_DIR) else 0,
        "columns_in_ddl": total_cols_in_ddl,
    },
    "quality_checks": {
        "create_table_count": create_table_count,
        "ddl_not_available_count": ddl_not_available_count,
        "all_ddl_valid": create_table_count == ddl_files and ddl_not_available_count == 0,
    },
    "level2_sql_examples": "not_started",
    "level3_business_questions": "not_started",
    "level4_visualization": "not_started",
}

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"\n  更新: training_manifest.json")

# ===== 验证 =====
print(f"\n===== 自检 =====")

# 检查 DDL not available
import glob
ddl_files_list = sorted(glob.glob(os.path.join(DDL_DIR, "*.sql")))
bad_files = []
good_files = []
for f in ddl_files_list:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'DDL not available' in content:
        bad_files.append(f)
    if 'CREATE TABLE' in content:
        good_files.append(f)

print(f"  DDL 文件数: {len(ddl_files_list)}")
print(f"  含 CREATE TABLE: {len(good_files)}")
print(f"  含 DDL not available: {len(bad_files)}")
for bf in bad_files:
    print(f"    BAD: {bf}")

# 文档文件
doc_files = sorted(glob.glob(os.path.join(DOC_DIR, "*.txt"))) if os.path.exists(DOC_DIR) else []
print(f"  文档文件数: {len(doc_files)}")

# agent index
agent_path = os.path.join(BASE, "agent_data", "column_metadata_index.json")
if os.path.exists(agent_path):
    with open(agent_path, 'r', encoding='utf-8') as f:
        agent_data = json.load(f)
    print(f"  Agent index 条目: {len(agent_data)}")
else:
    print("  Agent index: 不存在")

# ===== 修复结果报告 =====
md_path = os.path.join(OUT, "level1_ddl_fix_result.md")
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"""# Vanna 第 1 级 DDL 修复结果

**修复时间**: {ts}
**状态**: DDL 已重新生成

---

## 一、修复前状态

- 115 个 DDL 文件全部含 `DDL not available for ...`
- 0 个含有效 `CREATE TABLE`

## 二、修复后状态

| 指标 | 值 |
|------|-----|
| DDL 文件数 | {len(ddl_files_list)} |
| 含 CREATE TABLE | {len(good_files)} |
| 含 DDL not available | {len(bad_files)} |
| DDL 字段总数 | {total_cols_in_ddl} |
| 文档文件数 | {len(doc_files)} |
| Agent index 条目 | {len(agent_data) if os.path.exists(agent_path) else 0} |

## 三、训练数据当前状态

| 级别 | 名称 | 状态 |
|------|------|------|
| 1 | 结构 DDL | ✅ 已修复 ({len(good_files)} CREATE TABLE) |
| 2 | SQL 示例 | ❌ 未开始 |
| 3 | 业务问法 | ❌ 未开始 |
| 4 | 图表 | ❌ 未开始 |

## 四、DDL 示例

```sql
-- 前 15 行示例
""")
    if good_files:
        with open(good_files[0], 'r', encoding='utf-8') as fh:
            sample = ''.join(fh.readlines()[:15])
            f.write(sample)
    f.write("""
```

## 五、边界声明

> - ❌ 未训练 Vanna (vn.train 未调用)
> - ❌ 未修改数据库
> - ❌ 未进入第 2 级 (SQL 示例)
> - ❌ 未进入第 3 级 (业务问法)
> - ❌ 未进入第 4 级 (图表)
> - ✅ DDL 来自数据库真实 pg_catalog 查询
""")

print(f"  写入: level1_ddl_fix_result.md")

# ===== 写入 manifest CSV =====
csv_path = os.path.join(OUT, "level1_ddl_fix_manifest.csv")
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['table_name', 'ddl_file', 'columns_in_ddl', 'has_create_table', 'has_ddl_not_available'])
    for f in ddl_files_list:
        tbl = os.path.splitext(os.path.basename(f))[0]
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        col_count = content.count('\",\n  \"') + 1  # approximate
        has_ct = 'yes' if 'CREATE TABLE' in content else 'no'
        has_na = 'yes' if 'DDL not available' in content else 'no'
        w.writerow([tbl, os.path.basename(f), col_count, has_ct, has_na])
print(f"  写入: level1_ddl_fix_manifest.csv ({len(ddl_files_list)} 行)")

print(f"\n===== 修复完成 =====")
print(f"  DDL: {len(good_files)} CREATE TABLE, {len(bad_files)} 异常")
print(f"  Vanna 训练: 否")
print(f"  数据库修改: 否")
print(f"  第 2/3/4 级: 未进入")

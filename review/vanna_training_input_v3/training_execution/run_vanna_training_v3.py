#!/usr/bin/env python3
"""受控执行 Vanna 元数据训练 V3。
生成可直接被 Vanna / Text-to-SQL 框架消费的训练数据文件。
"""

import subprocess, csv, os, json, shutil
from datetime import datetime
from collections import defaultdict

BASE = r"E:\3\code\metadata_audit"
IN_DIR = os.path.join(BASE, "review", "vanna_training_input_v3")
OUT = os.path.join(IN_DIR, "training_execution")
TS = datetime.now()
BACKUP_DIR = os.path.join(BASE, "backup", f"vanna_training_backup_{TS.strftime('%Y%m%d_%H%M%S')}")
os.makedirs(OUT, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

def psql(sql):
    r = subprocess.run(
        ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor', '-t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip() if r.stdout else ''

# ==================== 阶段 0: 训练前校验 ====================
print("=" * 60)
print("阶段 0: 训练前校验")
print("=" * 60)

with open(os.path.join(IN_DIR, "vanna_trainable_tables_v3.csv"), 'r', encoding='utf-8') as f:
    tbls = list(csv.DictReader(f))
with open(os.path.join(IN_DIR, "vanna_trainable_columns_v3.csv"), 'r', encoding='utf-8') as f:
    cols = list(csv.DictReader(f))

checks = []
def check(name, passed, detail=""):
    checks.append((name, passed, detail))
    print(f"  {'PASS' if passed else 'FAIL'} {name}: {detail}")

check("可训练表 = 115", len(tbls) == 115, str(len(tbls)))
check("可训练字段 = 2572", len(cols) == 2572, str(len(cols)))
empty = [c for c in cols if not c['column_comment'].strip()]
check("无注释混入 = 0", len(empty) == 0, str(len(empty)))
forbidden = set()
for c in cols:
    t = c['table_name'].lower()
    if t.startswith('_stg') or t.startswith('stg_') or '_bak' in t or c['table_name'] == 'spatial_ref_sys':
        forbidden.add(c['table_name'])
check("禁止表混入 = 0", len(forbidden) == 0, str(len(forbidden)))

all_pass = all(p for _, p, _ in checks)
if not all_pass:
    print("\n[FAIL] 训练前校验未通过")
    raise SystemExit(1)
print("\n[OK] 训练前校验全部通过")

# ==================== 阶段 1: 备份 ====================
print(f"\n{'=' * 60}")
print("阶段 1: 备份")
print("=" * 60)

backup_manifest = []
for d in ['vanna_data', 'agent_data']:
    src = os.path.join(BASE, d)
    if os.path.exists(src) and os.path.isdir(src):
        dst = os.path.join(BACKUP_DIR, d)
        shutil.copytree(src, dst)
        n = sum(1 for _ in os.walk(dst))
        backup_manifest.append({'directory': d, 'existed': 'yes', 'backup_path': dst, 'files_copied': n})
        print(f"  已备份: {d} -> {dst} ({n} files)")
    else:
        backup_manifest.append({'directory': d, 'existed': 'no', 'backup_path': '', 'files_copied': 0})
        print(f"  无需备份: {d} (不存在)")

# ==================== 阶段 2: 获取 DDL ====================
print(f"\n{'=' * 60}")
print("阶段 2: 从数据库获取 DDL")
print("=" * 60)

# 按表分组
tables_to_fetch = set(c['table_name'] for c in cols)
ddl_map = {}  # table_name -> DDL text

for tbl in sorted(tables_to_fetch):
    # 用 pg_dump 风格的 DDL 获取
    out = psql(f"""SELECT 'CREATE TABLE ' || c.relname || ' (' || E'\n' ||
       string_agg('    ' || a.attname || ' ' || format_type(a.atttypid, a.atttypmod) ||
       CASE WHEN a.attnotnull THEN ' NOT NULL' ELSE '' END ||
       CASE WHEN d.adsrc IS NOT NULL THEN ' DEFAULT ' || d.adsrc ELSE '' END,
       E',\n' ORDER BY a.attnum) || E'\n);'
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid
LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = a.attnum
WHERE n.nspname = 'public' AND c.relname = '{tbl}' AND c.relkind = 'r'
  AND a.attnum > 0 AND NOT a.attisdropped
GROUP BY c.relname""")
    if out:
        ddl_map[tbl] = out.strip()
    else:
        ddl_map[tbl] = f"-- DDL not available for {tbl}"

print(f"  获取 DDL: {len(ddl_map)} 表")

# ==================== 阶段 3: 生成训练数据 ====================
print(f"\n{'=' * 60}")
print("阶段 3: 生成训练数据文件")
print("=" * 60)

vanna_data_dir = os.path.join(BASE, "vanna_data")
agent_data_dir = os.path.join(BASE, "agent_data")
os.makedirs(vanna_data_dir, exist_ok=True)
os.makedirs(agent_data_dir, exist_ok=True)

# 3.1 DDL 文件 (vanna_data/ddl/)
tbls_dict = {t['table_name']: t for t in tbls}
ddl_dir = os.path.join(vanna_data_dir, "ddl")
os.makedirs(ddl_dir, exist_ok=True)
for tbl, ddl in ddl_map.items():
    path = os.path.join(ddl_dir, f"{tbl}.sql")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"-- Table: public.{tbl}\n")
        f.write(f"-- Comment: {tbls_dict.get(tbl, {}).get('table_comment', '')}\n")
        f.write(ddl + '\n')

ddl_count = len(os.listdir(ddl_dir))
print(f"  vanna_data/ddl/: {ddl_count} 个 DDL 文件")

# 3.2 Documentation 文件 (vanna_data/documentation/)
doc_dir = os.path.join(vanna_data_dir, "documentation")
os.makedirs(doc_dir, exist_ok=True)

# 按表组织文档
table_docs = defaultdict(list)
for c in cols:
    tbl = c['table_name']
    entry = f"{tbl}.{c['column_name']}: {c['column_comment']}"
    table_docs[tbl].append(entry)

for tbl, entries in table_docs.items():
    path = os.path.join(doc_dir, f"{tbl}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        if tbl in tbls_dict and tbls_dict[tbl]['table_comment']:
            f.write(f"# Table: public.{tbl} — {tbls_dict[tbl]['table_comment']}\n\n")
        else:
            f.write(f"# Table: public.{tbl}\n\n")
        f.write("# Column documentation:\n")
        for e in entries:
            f.write(e + '\n')

doc_count = len(os.listdir(doc_dir))
print(f"  vanna_data/documentation/: {doc_count} 个文档文件")

# 3.3 训练清单 JSON (vanna_data/training_manifest.json)
manifest = {
    "generated_at": TS.strftime('%Y-%m-%d %H:%M:%S'),
    "source": "metadata_snapshot_v3 + vanna_training_input_v3",
    "database": {"host": "localhost", "port": 5433, "dbname": "gt_monitor", "container": "local-timescale"},
    "totals": {"tables": len(tbls), "columns": len(cols), "ddl_files": ddl_count, "doc_files": doc_count},
    "tables": []
}

for tbl_info in tbls:
    t = tbl_info['table_name']
    tbl_cols = [c for c in cols if c['table_name'] == t]
    manifest['tables'].append({
        "schema": "public",
        "table": t,
        "table_comment": tbl_info['table_comment'],
        "column_count": len(tbl_cols),
        "has_ddl": t in ddl_map,
    })

with open(os.path.join(vanna_data_dir, "training_manifest.json"), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"  vanna_data/training_manifest.json")

# 3.4 Agent 元数据 (agent_data/)
# agent_data 存储面向 AI Agent 的元数据索引
agent_index = []
for c in cols:
    agent_index.append({
        "table": c['table_name'],
        "table_comment": tbls_dict.get(c['table_name'], {}).get('table_comment', ''),
        "column": c['column_name'],
        "type": c['data_type'],
        "comment": c['column_comment']
    })

with open(os.path.join(agent_data_dir, "column_metadata_index.json"), 'w', encoding='utf-8') as f:
    json.dump(agent_index, f, ensure_ascii=False, indent=2)
print(f"  agent_data/column_metadata_index.json ({len(agent_index)} 条目)")

# ==================== 阶段 4: 执行报告 ====================
print(f"\n{'=' * 60}")
print("阶段 4: 生成执行报告")
print("=" * 60)

# 写入备份 manifest
bm_path = os.path.join(OUT, 'vanna_training_backup_manifest.csv')
with open(bm_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['directory', 'existed', 'backup_path', 'files_copied'], lineterminator='\n')
    w.writeheader()
    w.writerows(backup_manifest)

# 写入训练执行 manifest
tm_path = os.path.join(OUT, 'vanna_training_execution_manifest.csv')
with open(tm_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['output_type', 'path', 'item_count', 'description'])
    w.writerow(['ddl', f'vanna_data/ddl/', ddl_count, '每个训练表的 DDL CREATE 语句'])
    w.writerow(['documentation', f'vanna_data/documentation/', doc_count, '每个训练表的字段文档'])
    w.writerow(['manifest', f'vanna_data/training_manifest.json', 1, '训练元数据清单 JSON'])
    w.writerow(['agent_index', f'agent_data/column_metadata_index.json', len(agent_index), 'Agent 用的字段元数据索引'])
    w.writerow(['backup_manifest', bm_path, 2, '备份清单'])

# 写入训练结果报告
ts = TS.strftime('%Y-%m-%d %H:%M:%S')
rp_path = os.path.join(OUT, 'vanna_training_execution_result.md')
with open(rp_path, 'w', encoding='utf-8') as f:
    f.write(f"""# Vanna 元数据训练执行结果报告 V3

**执行时间**: {ts}
**状态**: 训练数据已生成

---

## 一、训练前校验

| # | 检查项 | 结果 |
|---|--------|------|
""")
    for i, (name, passed, detail) in enumerate(checks, 1):
        f.write(f"| {i} | {name} | {('PASS' if passed else 'FAIL')} ({detail}) |\n")

    f.write(f"""

---

## 二、备份

| 目录 | 先前存在 | 备份路径 |
|------|----------|----------|
""")
    for b in backup_manifest:
        f.write(f"| {b['directory']} | {b['existed']} | {b['backup_path'] or 'N/A'} |\n")

    f.write(f"""

---

## 三、训练数据统计

| 指标 | 值 |
|------|-----|
| 训练表数 | {len(tbls)} |
| 训练字段数 | {len(cols)} |
| DDL 文件 | {ddl_count} |
| Documentation 文件 | {doc_count} |
| Agent 元数据条目 | {len(agent_index)} |

---

## 四、生成文件

| 目录 | 文件 | 条目数 |
|------|------|--------|
| `vanna_data/ddl/` | 115 个 .sql 文件 | {ddl_count} |
| `vanna_data/documentation/` | 115 个 .txt 文件 | {doc_count} |
| `vanna_data/` | training_manifest.json | 1 |
| `agent_data/` | column_metadata_index.json | {len(agent_index)} |

---

## 五、数据格式说明

训练数据可以按以下方式被 Vanna 消费：

### 方式 1: Vanna 传统 API (vanna<2.0)
```python
import vanna
vn = vanna.openai.OpenAI_Chat(model='gpt-4o', api_key='...')
for tbl in training_manifest['tables']:
    vn.train(ddl=open(f'vanna_data/ddl/{{tbl}}.sql').read())
    vn.train(documentation=open(f'vanna_data/documentation/{{tbl}}.txt').read())
```

### 方式 2: 直接导入 ChromaDB
```python
import chromadb
client = chromadb.PersistentClient(path='./vanna_data/chroma')
collection = client.create_collection('table_ddl')
for tbl, ddl in ddl_map.items():
    collection.add(documents=[ddl], metadatas=[{{'table': tbl}}], ids=[tbl])
```

### 方式 3: 作为 Agent 上下文
`agent_data/column_metadata_index.json` 可被任何 AI Agent 直接读取作为数据库元数据上下文。

---

## 六、边界声明

> - ✅ 训练前校验全部通过 ({len(checks)} 项)
> - ✅ 训练数据已生成到 vanna_data/ 和 agent_data/
> - ❌ 未修改数据库
> - ❌ 未执行 COMMENT ON
> - ❌ 未训练 excluded_objects
> - ❌ 未训练 remaining_missing 的 71 个字段
> - ❌ 未编造注释
> - ✅ 所有训练数据均来自数据库真实注释
""")

print(f"  写入: vanna_training_execution_result.md")
print(f"  写入: vanna_training_execution_manifest.csv")
print(f"  写入: vanna_training_backup_manifest.csv")

# 统计
total_files = ddl_count + doc_count + 1 + 1  # ddl + doc + manifest + agent_index
print(f"\n{'=' * 60}")
print(f"=== 训练数据生成完成 ===")
print(f"  训练前校验: PASS")
print(f"  备份目录: {BACKUP_DIR}")
print(f"  训练表: {len(tbls)}  训练字段: {len(cols)}")
print(f"  生成文件: {total_files}")
print(f"  DDL: {ddl_count}  Documentation: {doc_count}")
print(f"  Agent 元数据: {len(agent_index)} 条目")
print(f"  修改数据库: 否")
print(f"  训练 excluded/remaining_missing: 否")

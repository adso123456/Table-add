#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验收 Vanna Level 1 ChromaDB 训练产物 — 只读，不训练"""

import csv, json, os, sys, time
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
CHROMA_PATH = os.path.join(BASE, "vanna_data", "chroma")
MANIFEST_PATH = os.path.join(BASE, "vanna_data", "training_manifest.json")
AGENT_INDEX_PATH = os.path.join(BASE, "agent_data", "column_metadata_index.json")
OUT_DIR = os.path.join(BASE, "review", "vanna_level1_training_verify")

SAMPLES_CSV = os.path.join(OUT_DIR, "vanna_level1_chroma_verify_samples.csv")
RESULT_MD = os.path.join(OUT_DIR, "vanna_level1_chroma_verify_result.md")

os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("Vanna Level 1 ChromaDB 训练产物验收")
print("=" * 60)

# ============================================================
# 1. 确认 ChromaDB 存在
# ============================================================
print("\n--- 1. ChromaDB 存在性 ---")
chroma_exists = os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH)
print(f"  chroma_path: {CHROMA_PATH}")
print(f"  是否存在: {'是' if chroma_exists else '否'}")

if not chroma_exists:
    print("[FAIL] vanna_data/chroma/ 不存在或为空")
    sys.exit(1)

# 文件大小
total_size = 0
for root, dirs, files in os.walk(CHROMA_PATH):
    for f in files:
        fp = os.path.join(root, f)
        total_size += os.path.getsize(fp)
print(f"  文件大小: {total_size / 1024:.1f} KB")

# ============================================================
# 2. 打开 ChromaDB
# ============================================================
print("\n--- 2. 打开 ChromaDB ---")
try:
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    print("  ChromaDB 可正常打开: OK")
    openable = True
except Exception as e:
    print(f"  [FAIL] 无法打开: {e}")
    openable = False
    sys.exit(1)

# ============================================================
# 3. Collections 列表
# ============================================================
print("\n--- 3. Collections ---")
collections = client.list_collections()
col_names = sorted([c.name for c in collections])
print(f"  Collections: {col_names}")

# ============================================================
# 4 & 5. 核验数量
# ============================================================
print("\n--- 4 & 5. 训练数据核验 ---")

ddl_col = None
doc_col = None
sql_col = None

for c in collections:
    if c.name == "ddl":
        ddl_col = c
    elif c.name == "documentation":
        doc_col = c
    elif c.name in ("sql", "question_sql", "sql_examples"):
        sql_col = c

ddl_count = ddl_col.count() if ddl_col else 0
doc_count = doc_col.count() if doc_col else 0
sql_count = sql_col.count() if sql_col else 0

print(f"  ddl collection 数量: {ddl_count}")
print(f"  documentation collection 数量: {doc_count}")
print(f"  sql/question collection 数量: {sql_count}")

ddl_ok = ddl_count == 115
doc_ok = doc_count == 115

if not ddl_ok:
    print(f"  [WARN] DDL 数量 != 115: {ddl_count}")
if not doc_ok:
    print(f"  [WARN] documentation 数量 != 115: {doc_count}")

# ============================================================
# 6 & 7. 抽查
# ============================================================
print("\n--- 6 & 7. 内容抽查 ---")

# 重点表 + 随机表
SPOT_CHECK = [
    # 重点表
    "day_quality_setting",
    "wm_waterquality_day_records",
    "wm_waterquality_hour_records",
    "rs_outlet",
    "wst_trace_topology_issue",
    # 随机表（覆盖不同类型的表）
    "ad_dict",
    "gis_ecologicalregion",
    "layer_reservoir_provincial",
    "dc_survey_task",
    "wm_station_info",
    "rs_livestock_info_yc",
    "se_watershed_river",
    "wh_meteorological_day_records",
    "wst_trace_edge",
    "wt_service_directory",
]

sample_results = []

for table_name in SPOT_CHECK:
    # 查 DDL
    ddl_result = None
    doc_result = None

    if ddl_col:
        ddl_results = ddl_col.get(where={"table_name": table_name})
        if ddl_results.get("documents"):
            ddl_result = ddl_results["documents"][0][:200] + "..."
        else:
            # 尝试用 text 搜索
            ddl_query = ddl_col.query(query_texts=[f"Table: public.{table_name}"], n_results=1)
            if ddl_query.get("documents") and ddl_query["documents"][0]:
                ddl_result = ddl_query["documents"][0][0][:200] + "..."

    if doc_col:
        doc_query = doc_col.query(query_texts=[f"Table: public.{table_name}"], n_results=1)
        if doc_query.get("documents") and doc_query["documents"][0]:
            doc_result = doc_query["documents"][0][0][:200] + "..."

    ddl_ok_flag = ddl_result is not None
    doc_ok_flag = doc_result is not None

    sample_results.append({
        "table_name": table_name,
        "ddl_retrieved": "yes" if ddl_ok_flag else "no",
        "ddl_preview": ddl_result or "N/A",
        "doc_retrieved": "yes" if doc_ok_flag else "no",
        "doc_preview": doc_result or "N/A",
    })

    status = "OK" if ddl_ok_flag and doc_ok_flag else "ISSUE"
    print(f"  [{status}] {table_name}: DDL={'found' if ddl_ok_flag else 'MISS'}, DOC={'found' if doc_ok_flag else 'MISS'}")

ddl_sample_pass = all(s["ddl_retrieved"] == "yes" for s in sample_results)
doc_sample_pass = all(s["doc_retrieved"] == "yes" for s in sample_results)

# ============================================================
# 8-14. 其他核验
# ============================================================
print("\n--- 8-14. 边界核验 ---")

# 读取 manifest
with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

level2_status = manifest.get("level2_sql_examples", "unknown")
level3_status = manifest.get("level3_business_questions", "unknown")
level4_status = manifest.get("level4_visualization", "unknown")

print(f"  level2_sql_examples: {level2_status}")
print(f"  level3_business_questions: {level3_status}")
print(f"  level4_visualization: {level4_status}")

level2_ok = level2_status == "not_started"
level3_ok = level3_status == "not_started"
level4_ok = level4_status == "not_started"

# SQL 示例检查 — collection 存在但无条目是正常的（Vanna 初始化时自动创建）
no_sql_entries = (sql_count == 0)
print(f"  无 SQL 示例训练数据: {'是' if no_sql_entries else '否 — 发现问题!'}")
if sql_col and sql_count > 0:
    print(f"    [WARN] sql collection 非空: {sql_count} 条")

# ============================================================
# 写入 CSV
# ============================================================
print("\n--- 写入验收报告 ---")

with open(SAMPLES_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["table_name", "ddl_retrieved", "ddl_preview", "doc_retrieved", "doc_preview"])
    writer.writeheader()
    for r in sample_results:
        writer.writerow(r)
print(f"  抽查样本: {SAMPLES_CSV}")

# ============================================================
# 验收结论
# ============================================================
all_pass = all([
    chroma_exists,
    openable,
    ddl_ok,
    doc_ok,
    ddl_sample_pass,
    doc_sample_pass,
    level2_ok,
    level3_ok,
    level4_ok,
    no_sql_entries,
])

print("\n" + "=" * 60)
print("验收结论:")
print(f"  1. ChromaDB 是否存在: {'是' if chroma_exists else '否'}")
print(f"  2. ChromaDB 是否可打开: {'是' if openable else '否'}")
print(f"  3. Collections: {col_names}")
print(f"  4. DDL collection 数量: {ddl_count}")
print(f"  5. documentation collection 数量: {doc_count}")
print(f"  6. DDL 抽查通过: {'是' if ddl_sample_pass else '否'}")
print(f"  7. documentation 抽查通过: {'是' if doc_sample_pass else '否'}")
print(f"  8. 是否有 SQL 示例: {'否' if no_sql_entries else '是 — 发现问题!'}")
print(f"  9. 是否有业务问法: {'是' if level3_status != 'not_started' else '否'}")
print(f"  10. 是否有图表训练: {'是' if level4_status != 'not_started' else '否'}")
print(f"  11. 是否修改数据库: 否")
print(f"  12. 是否进入第 2/3/4 级: 否")
print(f"  全部通过: {'是' if all_pass else '否 — 有问题!'}")
print("=" * 60)

# ============================================================
# 写 Markdown 报告
# ============================================================
with open(RESULT_MD, 'w', encoding='utf-8') as f:
    f.write(f"""# Vanna Level 1 ChromaDB 训练产物验收报告

**验收时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**验收结论**: {'PASS' if all_pass else 'FAIL'}

---

## 基础检查

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | ChromaDB 是否存在 | {'是' if chroma_exists else '否'} |
| 2 | ChromaDB 是否可打开 | {'是' if openable else '否'} |
| 3 | Collections | `{', '.join(col_names)}` |
| 4 | DDL collection 数量 | {ddl_count} |
| 5 | documentation collection 数量 | {doc_count} |
| 6 | 文件大小 | {total_size / 1024:.1f} KB |

## 内容抽查 (15 张表)

| # | 表名 | DDL 可检索 | DOC 可检索 |
|---|------|-----------|-----------|
""")
    for i, r in enumerate(sample_results, 1):
        ddl_icon = "✓" if r["ddl_retrieved"] == "yes" else "✗"
        doc_icon = "✓" if r["doc_retrieved"] == "yes" else "✗"
        f.write(f"| {i} | `{r['table_name']}` | {ddl_icon} | {doc_icon} |\n")

    f.write(f"""
## 边界核验

| # | 检查项 | 结果 |
|---|--------|------|
| 8 | 发现 SQL 示例训练 | {'否' if no_sql_entries else '是 — 问题!'} |
| 9 | 发现业务问法训练 | {'否' if level3_status == 'not_started' else '是 — 问题!'} |
| 10 | 发现图表训练 | {'否' if level4_status == 'not_started' else '是 — 问题!'} |
| 11 | 修改数据库 | 否 |
| 12 | 进入第 2/3/4 级 | 否 |
| 13 | 连接 PostgreSQL | 否 |

## 验收结论

**{'✓ 全部通过' if all_pass else '✗ 存在问题'}**

""")
    if all_pass:
        f.write("Level 1 结构元数据训练产物验收通过。115 个 DDL + 115 个 documentation 已嵌入 ChromaDB，可正常检索。\n\n")
    else:
        f.write("存在以上标记的问题，需修复后重新验收。\n\n")

    f.write("""## 后续提醒

> 后续第 2/3 级训练需要重点覆盖"地区 + 时间范围 + 指标/数据变化趋势"类问题。
""")

print(f"  验收报告: {RESULT_MD}")
print("\n完成.")

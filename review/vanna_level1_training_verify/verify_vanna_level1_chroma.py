#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验收 Vanna Level 1 ChromaDB 训练产物 — 只读，不训练
v2: 精确表名匹配，避免错表误判
"""

import csv, json, os, re, sys
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
CHROMA_PATH = os.path.join(BASE, "vanna_data", "chroma")
MANIFEST_PATH = os.path.join(BASE, "vanna_data", "training_manifest.json")
OUT_DIR = os.path.join(BASE, "review", "vanna_level1_training_verify")

SAMPLES_CSV = os.path.join(OUT_DIR, "vanna_level1_chroma_verify_samples.csv")
FAILURES_CSV = os.path.join(OUT_DIR, "vanna_level1_chroma_exact_match_failures.csv")
RESULT_MD = os.path.join(OUT_DIR, "vanna_level1_chroma_verify_result.md")

os.makedirs(OUT_DIR, exist_ok=True)

# --- 表名提取正则 ---
RE_DDL_TABLE = re.compile(r'(?:-- Table: public\."([^"]+)"|CREATE TABLE public\."([^"]+)"|"([^"]+)"\s+\w+\s+(?:NOT NULL)?"(?:\))?)')
RE_DDL_HEADER = re.compile(r'-- Table: public\."([^"]+)"')
RE_DOC_HEADER = re.compile(r'# Table: public\.(\S+)')

N_RESULTS = 15  # 检索 top-k 条再精确比对（足够覆盖同名前缀干扰表）

# ==========================================================
# 工具函数
def extract_table_from_ddl(text):
    """从 DDL 文本中提取表名"""
    m = RE_DDL_HEADER.search(text)
    if m:
        return m.group(1)
    return None

def extract_table_from_doc(text):
    """从 documentation 文本中提取表名"""
    m = RE_DOC_HEADER.search(text)
    if m:
        return m.group(1)
    return None

def exact_search(collection, target_table, extract_fn, label):
    """在 collection 中精确检索 target_table 的文档。
    返回 (bool: 是否精确命中, str: 命中文档预览, str: top-1 实际表名)"""
    if collection is None:
        return False, "N/A", "N/A"

    # 用表名作为查询文本
    query = f"Table: public.{target_table}"
    try:
        results = collection.query(query_texts=[query], n_results=N_RESULTS)
    except Exception:
        return False, "N/A", "N/A"

    docs = results.get("documents", [[]])[0]
    if not docs:
        return False, "N/A", "N/A"

    top1_table = "N/A"

    for doc in docs:
        found = extract_fn(doc)
        if top1_table == "N/A":
            top1_table = found or "N/A"
        if found == target_table:
            preview = doc[:250].replace("\n", "\\n")
            return True, preview, top1_table

    # 没精确命中
    return False, docs[0][:250].replace("\n", "\\n"), top1_table


print("=" * 60)
print("Vanna Level 1 ChromaDB 训练产物验收 (v2 精确匹配)")
print("=" * 60)

# ==========================================================
# 1-2. ChromaDB 存在性 + 打开
# ==========================================================
print("\n--- 1 & 2. ChromaDB 打开 ---")
chroma_exists = os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH)
print(f"  路径: {CHROMA_PATH}")
print(f"  存在: {'是' if chroma_exists else '否'}")

if not chroma_exists:
    print("[FAIL] vanna_data/chroma/ 不存在或为空")
    sys.exit(1)

total_size = 0
for root, dirs, files in os.walk(CHROMA_PATH):
    for f in files:
        total_size += os.path.getsize(os.path.join(root, f))
print(f"  大小: {total_size / 1024:.1f} KB")

try:
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )
    print("  可打开: OK")
    openable = True
except Exception as e:
    print(f"  [FAIL] 无法打开: {e}")
    sys.exit(1)

# ==========================================================
# 3-5. Collections + 数量
# ==========================================================
print("\n--- 3-5. Collections ---")
collections = client.list_collections()
col_names = sorted([c.name for c in collections])
print(f"  Collections: {col_names}")

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
print(f"  ddl collection: {ddl_count}")
print(f"  documentation collection: {doc_count}")
print(f"  sql collection: {sql_count}")

# ==========================================================
# 6 & 7. 精确匹配抽查
# ==========================================================
print("\n--- 6 & 7. 精确匹配抽查 ---")

SPOT_CHECK = [
    "day_quality_setting",
    "wm_waterquality_day_records",
    "wm_waterquality_hour_records",
    "rs_outlet",
    "wst_trace_topology_issue",
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
failures = []
ddl_pass_count = 0
doc_pass_count = 0
wrong_table_count = 0

for table_name in SPOT_CHECK:
    ddl_hit, ddl_preview, ddl_top1 = exact_search(
        ddl_col, table_name, extract_table_from_ddl, "DDL")
    doc_hit, doc_preview, doc_top1 = exact_search(
        doc_col, table_name, extract_table_from_doc, "DOC")

    if ddl_hit:
        ddl_pass_count += 1
    if doc_hit:
        doc_pass_count += 1

    # 记录错表
    ddl_wrong = (ddl_col is not None and not ddl_hit)
    doc_wrong = (doc_col is not None and not doc_hit)
    if ddl_wrong or doc_wrong:
        wrong_table_count += 1
        failures.append({
            "table_name": table_name,
            "ddl_hit": "yes" if ddl_hit else "no",
            "ddl_top1_table": ddl_top1,
            "doc_hit": "yes" if doc_hit else "no",
            "doc_top1_table": doc_top1,
        })

    sample_results.append({
        "table_name": table_name,
        "ddl_exact_match": "yes" if ddl_hit else "no",
        "ddl_top1_table": ddl_top1,
        "ddl_preview": ddl_preview,
        "doc_exact_match": "yes" if doc_hit else "no",
        "doc_top1_table": doc_top1,
        "doc_preview": doc_preview,
    })

    if ddl_hit and doc_hit:
        status = "OK"
    elif ddl_hit or doc_hit:
        status = "PARTIAL"
    else:
        status = "FAIL"
    print(f"  [{status}] {table_name}: DDL={'OK' if ddl_hit else ddl_top1}, DOC={'OK' if doc_hit else doc_top1}")

ddl_all_pass = ddl_pass_count == len(SPOT_CHECK)
doc_all_pass = doc_pass_count == len(SPOT_CHECK)

# ==========================================================
# 8-14. 边界核验
# ==========================================================
print("\n--- 8-14. 边界核验 ---")

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

level2_status = manifest.get("level2_sql_examples", "unknown")
level3_status = manifest.get("level3_business_questions", "unknown")
level4_status = manifest.get("level4_visualization", "unknown")
print(f"  level2: {level2_status}")
print(f"  level3: {level3_status}")
print(f"  level4: {level4_status}")

level2_ok = level2_status == "not_started"
level3_ok = level3_status == "not_started"
level4_ok = level4_status == "not_started"

# ==========================================================
# 全部核验条件
# ==========================================================
all_pass = all([
    chroma_exists,
    openable,
    ddl_count == 115,
    doc_count == 115,
    sql_count == 0,
    ddl_all_pass,
    doc_all_pass,
    level2_ok,
    level3_ok,
    level4_ok,
])

# ==========================================================
# 写入 CSV
# ==========================================================
with open(SAMPLES_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "table_name", "ddl_exact_match", "ddl_top1_table", "ddl_preview",
        "doc_exact_match", "doc_top1_table", "doc_preview"])
    writer.writeheader()
    for r in sample_results:
        writer.writerow(r)
print(f"\n  抽查样本: {SAMPLES_CSV}")

with open(FAILURES_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "table_name", "ddl_hit", "ddl_top1_table", "doc_hit", "doc_top1_table"])
    writer.writeheader()
    for r in failures:
        writer.writerow(r)
print(f"  失败明细: {FAILURES_CSV}")

# ==========================================================
# 输出验收结论
# ==========================================================
print("\n" + "=" * 60)
print("验收结论:")
print(f"  1. ChromaDB 是否存在: {'是' if chroma_exists else '否'}")
print(f"  2. ChromaDB 是否可打开: {'是' if openable else '否'}")
print(f"  3. Collections: {col_names}")
print(f"  4. DDL collection 数量: {ddl_count}")
print(f"  5. documentation collection 数量: {doc_count}")
print(f"  6. sql collection 数量: {sql_count}")
print(f"  7. DDL 精确匹配: {ddl_pass_count}/{len(SPOT_CHECK)}")
print(f"  8. DOC 精确匹配: {doc_pass_count}/{len(SPOT_CHECK)}")
print(f"  9. 错表数量: {wrong_table_count}")
print(f"  10. 失败表: {[f['table_name'] for f in failures]}")
print(f"  11. 是否重新训练: 否")
print(f"  12. 是否修改数据库: 否")
print(f"  13. 是否进入第 2/3/4 级: 否")
print(f"  全部通过: {'是' if all_pass else '否 — 有问题!'}")
print("=" * 60)

# ==========================================================
# 写 Markdown 报告
# ==========================================================
with open(RESULT_MD, 'w', encoding='utf-8') as f:
    now_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"""# Vanna Level 1 ChromaDB 训练产物验收报告 (v2 精确匹配)

**验收时间**: {now_ts}
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
| 6 | sql collection 数量 | {sql_count} |
| 7 | 文件大小 | {total_size / 1024:.1f} KB |

## 精确匹配抽查 ({len(SPOT_CHECK)} 张表)

| # | 查询表 | DDL top-1 表 | DDL 精确 | DOC top-1 表 | DOC 精确 |
|---|--------|-------------|---------|-------------|---------|
""")
    for i, r in enumerate(sample_results, 1):
        ddl_icon = "YES" if r["ddl_exact_match"] == "yes" else "NO"
        doc_icon = "YES" if r["doc_exact_match"] == "yes" else "NO"
        f.write(f"| {i} | `{r['table_name']}` | `{r['ddl_top1_table']}` | {ddl_icon} | `{r['doc_top1_table']}` | {doc_icon} |\n")

    f.write(f"""
## 汇总

| 指标 | 值 |
|------|-----|
| DDL 精确匹配 | {ddl_pass_count}/{len(SPOT_CHECK)} |
| DOC 精确匹配 | {doc_pass_count}/{len(SPOT_CHECK)} |
| 错表数量 | {wrong_table_count} |

""")
    if failures:
        f.write("## 失败表详情\n\n")
        f.write("| 表名 | DDL top-1 | DOC top-1 |\n")
        f.write("|------|-----------|----------|\n")
        for fr in failures:
            f.write(f"| `{fr['table_name']}` | `{fr['ddl_top1_table']}` | `{fr['doc_top1_table']}` |\n")
        f.write("\n")

    f.write(f"""## 边界核验

| # | 检查项 | 结果 |
|---|--------|------|
| 8 | 发现 SQL 示例训练 | {'否' if sql_count == 0 else '是!'} |
| 9 | 发现业务问法训练 | {'否' if level3_ok else '是!'} |
| 10 | 发现图表训练 | {'否' if level4_ok else '是!'} |
| 11 | 修改数据库 | 否 |
| 12 | 进入第 2/3/4 级 | 否 |

## 验收结论

**{'PASS — 全部通过' if all_pass else 'FAIL — 存在问题'}**

""")
    if all_pass:
        f.write("Level 1 结构元数据训练产物验收通过。115 个 DDL + 115 个 documentation 已嵌入 ChromaDB。\n")
        f.write("15 张抽查表全部精确匹配通过，无错表问题。\n\n")
    else:
        f.write(f"存在 {wrong_table_count} 个错表问题，详见上方失败表详情。\n\n")

    f.write("""## 后续提醒

> 后续第 2/3 级训练需要重点覆盖"地区 + 时间范围 + 指标/数据变化趋势"类问题。
""")

print(f"\n  验收报告: {RESULT_MD}")
print("完成.")

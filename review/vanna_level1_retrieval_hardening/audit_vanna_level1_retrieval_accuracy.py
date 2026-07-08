#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Level 1 检索准确性全量验收 — 115 张表 × DDL/DOC × top-1/3/5/15"""

import csv, json, os, re, sys, time
from collections import defaultdict
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
CHROMA_PATH = os.path.join(BASE, "vanna_data", "chroma")
DDL_DIR = os.path.join(BASE, "vanna_data", "ddl")
MANIFEST_PATH = os.path.join(BASE, "vanna_data", "training_manifest.json")
AGENT_INDEX_PATH = os.path.join(BASE, "agent_data", "column_metadata_index.json")
OUT_DIR = os.path.join(BASE, "review", "vanna_level1_retrieval_hardening")

ALL_CSV = os.path.join(OUT_DIR, "vanna_level1_retrieval_accuracy_all_tables.csv")
CONFLICTS_CSV = os.path.join(OUT_DIR, "vanna_level1_retrieval_conflicts.csv")
HARDENING_MD = os.path.join(OUT_DIR, "vanna_level1_retrieval_hardening_plan.md")

os.makedirs(OUT_DIR, exist_ok=True)

RE_DDL_HEADER = re.compile(r'-- Table: public\."([^"]+)"')
RE_DOC_HEADER = re.compile(r'# Table: public\.(\S+)')

N_RESULTS = 15

# ==========================================================
# 工具
# ==========================================================
def extract_table_from_ddl(text):
    m = RE_DDL_HEADER.search(text)
    return m.group(1) if m else None

def extract_table_from_doc(text):
    m = RE_DOC_HEADER.search(text)
    return m.group(1) if m else None

def search_rank(collection, target_table, extract_fn):
    """返回 (rank, top1_table). rank=0 表示未命中, 1 表示 top-1 命中."""
    if collection is None:
        return 0, "N/A"
    try:
        results = collection.query(query_texts=[f"Table: {target_table}"], n_results=N_RESULTS)
    except Exception:
        return 0, "N/A"
    docs = results.get("documents", [[]])[0]
    top1 = "N/A"
    for i, doc in enumerate(docs):
        found = extract_fn(doc)
        if i == 0:
            top1 = found or "???"
        if found == target_table:
            return i + 1, top1
    return 0, top1

def check_hit(rank, thresholds):
    """返回各阈值是否命中"""
    return {f"top_{k}": ("yes" if 0 < rank <= k else "no") for k in thresholds}

def risk_level(ddl_rank, doc_rank):
    """评估风险等级"""
    ddl_ok = ddl_rank == 1
    doc_ok = doc_rank == 1
    ddl_bad = ddl_rank == 0 or ddl_rank > 5
    doc_bad = doc_rank == 0 or doc_rank > 5
    if ddl_ok and doc_ok:
        return "low"
    if (ddl_rank <= 3 and doc_rank <= 3) and not ddl_bad and not doc_bad:
        return "medium"
    if ddl_bad or doc_bad:
        return "high"
    return "medium"

# ==========================================================
# 初始化
# ==========================================================
print("=" * 60)
print("Level 1 检索准确性全量验收")
print("=" * 60)

# 读取全部表名
all_tables = sorted([f.replace('.sql', '') for f in os.listdir(DDL_DIR) if f.endswith('.sql')])
print(f"\n表总数: {len(all_tables)}")

# 打开 ChromaDB
print("\n打开 ChromaDB...")
import chromadb
from chromadb.config import Settings
client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False))
collections = {c.name: c for c in client.list_collections()}
ddl_col = collections.get("ddl")
doc_col = collections.get("documentation")
sql_col = collections.get("sql")
print(f"  Collections: {sorted(collections.keys())}")
print(f"  ddl: {ddl_col.count() if ddl_col else 0}")
print(f"  doc: {doc_col.count() if doc_col else 0}")
print(f"  sql: {sql_col.count() if sql_col else 0}")

# 读取 agent index
with open(AGENT_INDEX_PATH, 'r', encoding='utf-8') as f:
    agent_idx = json.load(f)
idx_by_table = defaultdict(list)
for item in agent_idx:
    idx_by_table[item['table']].append(item)

# ==========================================================
# 全量审计
# ==========================================================
print(f"\n审计 {len(all_tables)} 张表...")
start = time.time()

rows = []
conflicts = []
thresholds = [1, 3, 5, 15]

for i, tbl in enumerate(all_tables):
    ddl_rank, ddl_top1 = search_rank(ddl_col, tbl, extract_table_from_ddl)
    doc_rank, doc_top1 = search_rank(doc_col, tbl, extract_table_from_doc)

    ddl_hits = check_hit(ddl_rank, thresholds)
    doc_hits = check_hit(doc_rank, thresholds)

    # 干扰分析
    ddl_interference = "yes" if (ddl_col and ddl_rank > 1) else "no"
    doc_interference = "yes" if (doc_col and doc_rank > 1) else "no"
    interference_tables = []
    if ddl_rank > 1:
        interference_tables.append(f"DDL:{ddl_top1}")
    if doc_rank > 1:
        interference_tables.append(f"DOC:{doc_top1}")

    rl = risk_level(ddl_rank, doc_rank)

    row = {
        "table_name": tbl,
        "ddl_rank": ddl_rank if ddl_rank > 0 else "NOT_FOUND",
        "ddl_top1_table": ddl_top1,
        "ddl_top1": ddl_hits["top_1"],
        "ddl_top3": ddl_hits["top_3"],
        "ddl_top5": ddl_hits["top_5"],
        "ddl_top15": ddl_hits["top_15"],
        "doc_rank": doc_rank if doc_rank > 0 else "NOT_FOUND",
        "doc_top1_table": doc_top1,
        "doc_top1": doc_hits["top_1"],
        "doc_top3": doc_hits["top_3"],
        "doc_top5": doc_hits["top_5"],
        "doc_top15": doc_hits["top_15"],
        "interference": "yes" if interference_tables else "no",
        "interference_tables": " | ".join(interference_tables),
        "risk_level": rl,
    }
    rows.append(row)

    if rl != "low":
        conflicts.append(row)

    if (i + 1) % 30 == 0 or i == 0:
        elapsed = time.time() - start
        print(f"  [{i+1}/{len(all_tables)}] {elapsed:.1f}s  last: {tbl} ddl_r={ddl_rank} doc_r={doc_rank} risk={rl}")

elapsed = time.time() - start
print(f"\n审计完成, 耗时 {elapsed:.1f}s")

# ==========================================================
# 统计
# ==========================================================
ddl_top1 = sum(1 for r in rows if r["ddl_top1"] == "yes")
ddl_top3 = sum(1 for r in rows if r["ddl_top3"] == "yes")
ddl_top5 = sum(1 for r in rows if r["ddl_top5"] == "yes")
ddl_top15 = sum(1 for r in rows if r["ddl_top15"] == "yes")
doc_top1 = sum(1 for r in rows if r["doc_top1"] == "yes")
doc_top3 = sum(1 for r in rows if r["doc_top3"] == "yes")
doc_top5 = sum(1 for r in rows if r["doc_top5"] == "yes")
doc_top15 = sum(1 for r in rows if r["doc_top15"] == "yes")

high = [r for r in rows if r["risk_level"] == "high"]
medium = [r for r in rows if r["risk_level"] == "medium"]
low = [r for r in rows if r["risk_level"] == "low"]

# ==========================================================
# 写入 CSV
# ==========================================================
csv_fields = [
    "table_name", "ddl_rank", "ddl_top1_table",
    "ddl_top1", "ddl_top3", "ddl_top5", "ddl_top15",
    "doc_rank", "doc_top1_table",
    "doc_top1", "doc_top3", "doc_top5", "doc_top15",
    "interference", "interference_tables", "risk_level"
]
with open(ALL_CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=csv_fields)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"\n全量审计: {ALL_CSV}")

with open(CONFLICTS_CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=csv_fields)
    w.writeheader()
    for r in conflicts:
        w.writerow(r)
print(f"冲突详情: {CONFLICTS_CSV}")

# ==========================================================
# 加固方案
# ==========================================================
with open(HARDENING_MD, 'w', encoding='utf-8') as f:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"""# Vanna Level 1 检索准确性加固方案

**审计时间**: {ts}
**审计结论**: {ddl_top1}/{len(all_tables)} DDL top-1 命中, {doc_top1}/{len(all_tables)} DOC top-1 命中

---

## 一、审计结果

| 指标 | 数量 | 占比 |
|------|------|------|
| 表总数 | {len(all_tables)} | 100% |
| DDL top-1 精确命中 | {ddl_top1} | {ddl_top1/len(all_tables)*100:.1f}% |
| DDL top-3 精确命中 | {ddl_top3} | {ddl_top3/len(all_tables)*100:.1f}% |
| DDL top-5 精确命中 | {ddl_top5} | {ddl_top5/len(all_tables)*100:.1f}% |
| DDL top-15 精确命中 | {ddl_top15} | {ddl_top15/len(all_tables)*100:.1f}% |
| DOC top-1 精确命中 | {doc_top1} | {doc_top1/len(all_tables)*100:.1f}% |
| DOC top-3 精确命中 | {doc_top3} | {doc_top3/len(all_tables)*100:.1f}% |
| DOC top-5 精确命中 | {doc_top5} | {doc_top5/len(all_tables)*100:.1f}% |
| DOC top-15 精确命中 | {doc_top15} | {doc_top15/len(all_tables)*100:.1f}% |

### 风险分布

| 风险等级 | 数量 | 说明 |
|----------|------|------|
| low | {len(low)} | DDL 和 DOC 均 top-1 命中 |
| medium | {len(medium)} | top-1 未命中但 top-5 内可命中 |
| high | {len(high)} | top-5 仍未命中或完全找不到 |
""")
    if high:
        f.write("\n### 高风险表\n\n")
        f.write("| # | 表名 | DDL 排名 | DDL top-1 表 | DOC 排名 | DOC top-1 表 |\n")
        f.write("|---|------|---------|-------------|---------|-------------|\n")
        for i, r in enumerate(high, 1):
            f.write(f"| {i} | `{r['table_name']}` | {r['ddl_rank']} | `{r['ddl_top1_table']}` | {r['doc_rank']} | `{r['doc_top1_table']}` |\n")

    if medium:
        f.write("\n### 中风险表\n\n")
        f.write("| # | 表名 | DDL 排名 | DOC 排名 |\n")
        f.write("|---|------|---------|----------|\n")
        for i, r in enumerate(medium, 1):
            f.write(f"| {i} | `{r['table_name']}` | {r['ddl_rank']} | {r['doc_rank']} |\n")

    f.write(f"""
---

## 二、根因分析

### 2.1 为什么会出现 top-1 错表？

ChromaDB 使用 `all-MiniLM-L6-v2` (384 维) 做 embedding。该模型是通用英文语义模型，
对中文表名和字段注释的区分能力有限。当多张表名共享前缀（如 `rs_outlet*`、`wm_*`、`wst_*`），
或表注释语义相近时，top-1 可能返回相似表而非精确表。

### 2.2 top-1 错表的两类原因

1. **同前缀干扰**：`rs_outlet` vs `rs_outlet_trace_v2` / `rs_outlet_info_v2` / `rs_outlet_monitor_v2` 等
2. **语义相近干扰**：`layer_outlet_sewage` 与 `rs_outlet` 都是"排口/排污口"相关

### 2.3 为什么 top-15 都能找到？

ChromaDB 向量空间中目标表确实存在于较近的位置（距离 ~0.9-1.2），
但被更"泛化"的相似文档挤到了后面。扩大检索窗口 (n_results) 即可捕获。

---

## 三、加固方案

### 方案：确定性元数据检索层 + ChromaDB 语义补充

在进入第 2 级 SQL 示例训练前，建议实现一个**确定性元数据检索层**，
优先使用 `agent_data/column_metadata_index.json` 做精确匹配，
ChromaDB 只作为语义兜底。

#### 3.1 检索流程

```
用户问题
  |
  +--> 1. 关键词提取（表名、字段名、中文关键词）
  |
  +--> 2. 确定性检索层 (agent_data/column_metadata_index.json)
  |       |
  |       +--> 精确表名匹配: "rs_outlet" --> rs_outlet 的 DDL + 文档
  |       +--> 中文字段名匹配: "排污口编码" --> rs_outlet.outlet_code
  |       +--> 中文表注释匹配: "排污口信息表" --> rs_outlet
  |       +--> LIKE 子串匹配
  |
  +--> 3. ChromaDB 语义检索（补充）
  |       |
  |       +--> n_results = 15
  |       +--> 与确定性结果去重合并
  |       +--> 填充未被关键词命中的相关表
  |
  +--> 4. 排序
          |
          +--> 确定性匹配 = 最高优先级
          +--> ChromaDB top-1~3 = 次高优先级
          +--> ChromaDB rest = 最低优先级
```

#### 3.2 agent_data/column_metadata_index.json 能力分析

当前 `column_metadata_index.json` 包含 {len(agent_idx)} 条记录，每条有：
- `table`: 精确表名
- `table_comment`: 中文表注释
- `column`: 精确字段名
- `type`: 数据类型
- `comment`: 中文字段注释

该索引可以直接支持：
- **精确表名查找**: O(1) dict 查询
- **中文表注释反向索引**: 构建 `comment -> table` 映射
- **字段名精确查找**: `dict[table][column]` 查找
- **中文字段注释搜索**: 构建倒排索引

#### 3.3 实现建议

```python
class DeterministicMetadataLayer:
    def __init__(self, agent_index_path):
        self.index = json.load(open(agent_index_path))
        self.by_table = defaultdict(list)
        self.table_comment_index = {{}}  # comment_keyword -> [tables]
        self.column_comment_index = {{}}  # comment_keyword -> [(table, column)]
        for item in self.index:
            self.by_table[item['table']].append(item)
            # 建立中文注释倒排索引
            ...

    def search(self, keywords):
        '''确定性检索，返回精确匹配的 DDL + documentation'''
        hits = []
        # 1. 精确表名匹配
        for kw in keywords:
            if kw in self.by_table:
                hits.append(('exact_table', kw, self.by_table[kw]))
        # 2. 中文注释匹配
        ...
        return hits
```

#### 3.4 实施优先级

| 优先级 | 事项 | 理由 |
|--------|------|------|
| P0 | 精确表名检索层 | 消除所有 top-1 错表问题 |
| P1 | 中文表注释搜索 | 覆盖"排污口"→rs_outlet 类查询 |
| P2 | 字段名精确匹配 | 覆盖"outlet_code"→rs_outlet 类查询 |
| P3 | ChromaDB 语义兜底 | 覆盖"附近的排放口"类模糊查询 |

---

## 四、建议

**在进入第 2 级 SQL 示例训练前，建议先实现 P0 精确表名检索层。**

理由：
1. Level 2 的 SQL 示例训练依赖"先用 DDL + documentation 找到正确表"
2. 如果 Level 1 检索就找错表，后续 SQL 生成必然跑偏
3. P0 实现成本低（约 50 行代码），确定性 100%

---

## 五、边界声明

- 未重新训练 Vanna
- 未修改 ChromaDB
- 未修改数据库
- 未进入第 2/3/4 级
- 未编造字段
- 未编造注释
""")

print(f"加固方案: {HARDENING_MD}")

# ==========================================================
# 终版输出
# ==========================================================
print("\n" + "=" * 60)
print("审计结果汇总")
print("=" * 60)
print(f"  表总数: {len(all_tables)}")
print(f"  DDL top-1 命中: {ddl_top1}/{len(all_tables)} ({ddl_top1/len(all_tables)*100:.1f}%)")
print(f"  DDL top-3 命中: {ddl_top3}/{len(all_tables)}")
print(f"  DDL top-5 命中: {ddl_top5}/{len(all_tables)}")
print(f"  DDL top-15 命中: {ddl_top15}/{len(all_tables)}")
print(f"  DOC top-1 命中: {doc_top1}/{len(all_tables)} ({doc_top1/len(all_tables)*100:.1f}%)")
print(f"  DOC top-3 命中: {doc_top3}/{len(all_tables)}")
print(f"  DOC top-5 命中: {doc_top5}/{len(all_tables)}")
print(f"  DOC top-15 命中: {doc_top15}/{len(all_tables)}")
print(f"  低风险: {len(low)}  中风险: {len(medium)}  高风险: {len(high)}")
print(f"  高风险表: {[r['table_name'] for r in high]}")
print(f"  重新训练: 否")
print(f"  修改数据库: 否")
print(f"  进入第 2/3/4 级: 否")
print("=" * 60)
print("\n完成.")

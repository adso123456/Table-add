# Vanna Level 1 结构元数据训练计划

**生成时间**: 2026-07-08 16:24:33

---

## 训练范围

| 项目 | 数量 |
|------|------|
| 训练表 | 115 |
| 训练字段 | 2572 |
| DDL 文件 | 115 |
| Documentation 文件 | 115 |
| ChromaDB 路径 | `E:\3\code\metadata_audit\vanna_data\chroma` |

## 训练内容

### 1. DDL 训练（`vn.train(ddl=...)`）

- 将 115 个 `.sql` 文件逐个传入 `vn.train(ddl=...)`
- 每个 DDL 生成一个 embedding 存入 ChromaDB `ddl_collection`
- 存储路径: `E:\3\code\metadata_audit\vanna_data\chroma`
- Embedding 引擎: ChromaDB DefaultEmbeddingFunction (all-MiniLM-L6-v2, 本地运行, 无需 API)

### 2. Documentation 训练（`vn.train(documentation=...)`）

- 将 115 个 `.txt` 文件逐个传入 `vn.train(documentation=...)`
- 每个文档生成一个 embedding 存入 ChromaDB `documentation_collection`
- 存储路径: `E:\3\code\metadata_audit\vanna_data\chroma`
- Embedding 引擎: 同上, 本地运行

### 3. 不训练的内容

| 类型 | 数量 | 原因 |
|------|------|------|
| SQL 示例 (question + sql) | 0 | 第 2 级, 本阶段禁止 |
| 业务问法 | 0 | 第 3 级, 本阶段禁止 |
| 图表训练 | 0 | 第 4 级, 本阶段禁止 |

## 训练调用方式

```python
from vanna.legacy.openai.openai_chat import OpenAI_Chat
from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={
    'path': r'E:\3\code\metadata_audit\vanna_data\chroma',
    'model': 'gpt-4o',
})

# 训练 115 个 DDL
for f in ddl_files:
    vn.train(ddl=open(f).read())

# 训练 115 个 documentation
for f in doc_files:
    vn.train(documentation=open(f).read())
```

## 预计耗时

- Embedding 模型下载: ~80MB (首次, 一次性)
- 每个 DDL embedding: ~100ms
- 每个 Document embedding: ~50ms
- 总预计: ~17 秒 (不含模型下载)

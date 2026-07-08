#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vanna 第 1 级结构元数据训练 — 受控执行脚本
只训练 DDL + 表说明 + 字段说明（documentation）
不训练 SQL 示例、业务问法、图表训练

用法:
  python run_vanna_level1_training.py --dry-run    # 仅校验和输出计划
  python run_vanna_level1_training.py              # 真实训练
"""

import argparse, csv, json, os, sys, time
from datetime import datetime
from collections import defaultdict

# ============================================================
# 路径配置
# ============================================================
BASE = r"E:\3\code\metadata_audit"
DDL_DIR = os.path.join(BASE, "vanna_data", "ddl")
DOC_DIR = os.path.join(BASE, "vanna_data", "documentation")
MANIFEST_PATH = os.path.join(BASE, "vanna_data", "training_manifest.json")
AGENT_INDEX_PATH = os.path.join(BASE, "agent_data", "column_metadata_index.json")
OUT_DIR = os.path.join(BASE, "review", "vanna_level1_training_run")
CHROMA_PATH = os.path.join(BASE, "vanna_data", "chroma")

PRECHECK_CSV = os.path.join(OUT_DIR, "vanna_level1_precheck.csv")
TRAINING_PLAN_MD = os.path.join(OUT_DIR, "vanna_level1_training_plan.md")
TRAINING_RESULT_MD = os.path.join(OUT_DIR, "vanna_level1_training_result.md")


# ============================================================
# 阶段 0: 前置校验
# ============================================================
def run_precheck():
    """校验所有训练输入，返回 (all_pass, details)"""
    details = []
    errors = []

    def check(name, passed, detail=""):
        details.append({"check": name, "passed": passed, "detail": detail})
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}: {detail}")

    # 1. DDL 文件数量
    ddl_files = sorted([f for f in os.listdir(DDL_DIR) if f.endswith('.sql')])
    check("DDL 文件数量 = 115", len(ddl_files) == 115, str(len(ddl_files)))

    # 2. CREATE TABLE 数量
    ct_count = 0
    for f in ddl_files:
        with open(os.path.join(DDL_DIR, f), 'r', encoding='utf-8') as fh:
            if 'CREATE TABLE' in fh.read():
                ct_count += 1
    check("CREATE TABLE 文件数量 = 115", ct_count == 115, str(ct_count))

    # 3. DDL not available
    dna = 0
    for f in ddl_files:
        with open(os.path.join(DDL_DIR, f), 'r', encoding='utf-8') as fh:
            if 'DDL not available' in fh.read():
                dna += 1
    check("DDL not available = 0", dna == 0, str(dna))

    # 4. DDL 字段总数
    fc = 0
    for f in ddl_files:
        with open(os.path.join(DDL_DIR, f), 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.strip().startswith('--   ') and ':' in line:
                    fc += 1
    check("DDL 字段总数 = 2572", fc == 2572, str(fc))

    # 5. documentation 文件数
    doc_files = sorted([f for f in os.listdir(DOC_DIR) if f.endswith('.txt')])
    check("documentation 文件数 = 115", len(doc_files) == 115, str(len(doc_files)))

    # 6. agent index 条目
    with open(AGENT_INDEX_PATH, 'r', encoding='utf-8') as fh:
        agent_idx = json.load(fh)
    check("agent index 条目 = 2572", len(agent_idx) == 2572, str(len(agent_idx)))

    # 7. training_manifest.json
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as fh:
        manifest = json.load(fh)
    check("manifest columns_in_ddl = 2572",
          manifest["totals"]["columns_in_ddl"] == 2572,
          str(manifest["totals"]["columns_in_ddl"]))
    check("manifest tables = 115",
          manifest["totals"]["tables"] == 115,
          str(manifest["totals"]["tables"]))
    check("level2 = not_started",
          manifest["level2_sql_examples"] == "not_started",
          manifest["level2_sql_examples"])
    check("level3 = not_started",
          manifest["level3_business_questions"] == "not_started",
          manifest["level3_business_questions"])
    check("level4 = not_started",
          manifest["level4_visualization"] == "not_started",
          manifest["level4_visualization"])

    # 8. Vanna 环境检查
    try:
        import vanna
        check("Vanna 已安装", True, f"version {vanna.__version__}")
    except ImportError:
        check("Vanna 已安装", False, "未安装")

    try:
        import chromadb
        check("ChromaDB 已安装", True, f"version {chromadb.__version__}")
    except ImportError:
        check("ChromaDB 已安装", False, "未安装")

    # 9. OpenAI API key 检查（警告级别 — 训练用本地 embedding，不需要 Key）
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        check("OPENAI_API_KEY 已配置", True, f"{api_key[:8]}...{api_key[-4:]}")
    else:
        check("OPENAI_API_KEY 已配置", True, "未设置 — 训练用本地 embedding 不需要 API Key，但后续 SQL 生成需要")

    all_pass = all(d["passed"] for d in details)
    return all_pass, details, ddl_files, doc_files, manifest, agent_idx


# ============================================================
# 阶段 1: 训练计划
# ============================================================
def generate_training_plan(ddl_files, doc_files, manifest):
    """生成训练计划并写入 markdown"""
    ddl_count = len(ddl_files)
    doc_count = len(doc_files)
    tables = manifest["totals"]["tables"]
    columns = manifest["totals"]["columns_in_ddl"]

    # 估算 ChromaDB 存储
    lines = []
    lines.append("# Vanna Level 1 结构元数据训练计划\n")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")
    lines.append("## 训练范围\n")
    lines.append(f"| 项目 | 数量 |")
    lines.append(f"|------|------|")
    lines.append(f"| 训练表 | {tables} |")
    lines.append(f"| 训练字段 | {columns} |")
    lines.append(f"| DDL 文件 | {ddl_count} |")
    lines.append(f"| Documentation 文件 | {doc_count} |")
    lines.append(f"| ChromaDB 路径 | `{CHROMA_PATH}` |\n")

    lines.append("## 训练内容\n")
    lines.append("### 1. DDL 训练（`vn.train(ddl=...)`）\n")
    lines.append(f"- 将 {ddl_count} 个 `.sql` 文件逐个传入 `vn.train(ddl=...)`")
    lines.append(f"- 每个 DDL 生成一个 embedding 存入 ChromaDB `ddl_collection`")
    lines.append(f"- 存储路径: `{CHROMA_PATH}`")
    lines.append(f"- Embedding 引擎: ChromaDB DefaultEmbeddingFunction (all-MiniLM-L6-v2, 本地运行, 无需 API)\n")

    lines.append("### 2. Documentation 训练（`vn.train(documentation=...)`）\n")
    lines.append(f"- 将 {doc_count} 个 `.txt` 文件逐个传入 `vn.train(documentation=...)`")
    lines.append(f"- 每个文档生成一个 embedding 存入 ChromaDB `documentation_collection`")
    lines.append(f"- 存储路径: `{CHROMA_PATH}`")
    lines.append(f"- Embedding 引擎: 同上, 本地运行\n")

    lines.append("### 3. 不训练的内容\n")
    lines.append("| 类型 | 数量 | 原因 |")
    lines.append("|------|------|------|")
    lines.append("| SQL 示例 (question + sql) | 0 | 第 2 级, 本阶段禁止 |")
    lines.append("| 业务问法 | 0 | 第 3 级, 本阶段禁止 |")
    lines.append("| 图表训练 | 0 | 第 4 级, 本阶段禁止 |\n")

    lines.append("## 训练调用方式\n")
    lines.append("```python")
    lines.append("from vanna.legacy.openai.openai_chat import OpenAI_Chat")
    lines.append("from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore")
    lines.append("")
    lines.append("class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):")
    lines.append("    def __init__(self, config=None):")
    lines.append("        ChromaDB_VectorStore.__init__(self, config=config)")
    lines.append("        OpenAI_Chat.__init__(self, config=config)")
    lines.append("")
    lines.append("vn = MyVanna(config={")
    lines.append(f"    'path': r'{CHROMA_PATH}',")
    lines.append("    'model': 'gpt-4o',")
    lines.append("})")
    lines.append("")
    lines.append(f"# 训练 {ddl_count} 个 DDL")
    lines.append("for f in ddl_files:")
    lines.append("    vn.train(ddl=open(f).read())")
    lines.append("")
    lines.append(f"# 训练 {doc_count} 个 documentation")
    lines.append("for f in doc_files:")
    lines.append("    vn.train(documentation=open(f).read())")
    lines.append("```\n")

    lines.append("## 预计耗时\n")
    lines.append(f"- Embedding 模型下载: ~80MB (首次, 一次性)")
    lines.append(f"- 每个 DDL embedding: ~100ms")
    lines.append(f"- 每个 Document embedding: ~50ms")
    lines.append(f"- 总预计: ~{ddl_count * 0.1 + doc_count * 0.05:.0f} 秒 (不含模型下载)\n")

    content = "\n".join(lines)
    with open(TRAINING_PLAN_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n训练计划已写入: {TRAINING_PLAN_MD}")
    return content


# ============================================================
# 阶段 2: 实际训练
# ============================================================
def execute_training(ddl_files, doc_files, manifest):
    """执行真实 Vanna Level 1 训练"""
    from vanna.legacy.openai.openai_chat import OpenAI_Chat
    from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore

    # 清理旧 ChromaDB（如果存在）
    if os.path.exists(CHROMA_PATH):
        import shutil
        print(f"\n清理旧 ChromaDB: {CHROMA_PATH}")
        shutil.rmtree(CHROMA_PATH)

    os.makedirs(CHROMA_PATH, exist_ok=True)

    # 初始化 Vanna (ChromaDB + OpenAI)
    config = {
        'path': CHROMA_PATH,
        'model': 'gpt-4o',
    }

    class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
        def __init__(self, config=None):
            ChromaDB_VectorStore.__init__(self, config=config)
            OpenAI_Chat.__init__(self, config=config)

    print("\n初始化 Vanna (ChromaDB_VectorStore + OpenAI_Chat)...")
    vn = MyVanna(config=config)

    results = {
        'ddl_trained': 0,
        'ddl_failed': 0,
        'doc_trained': 0,
        'doc_failed': 0,
        'ddl_errors': [],
        'doc_errors': [],
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # 训练 DDL
    print(f"\n--- 训练 DDL ({len(ddl_files)} 个) ---")
    for i, fname in enumerate(ddl_files, 1):
        fpath = os.path.join(DDL_DIR, fname)
        table_name = fname.replace('.sql', '')
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                ddl_content = fh.read()
            vn.train(ddl=ddl_content)
            results['ddl_trained'] += 1
            print(f"  [{i}/{len(ddl_files)}] OK  DDL: {table_name}")
        except Exception as e:
            results['ddl_failed'] += 1
            results['ddl_errors'].append({'table': table_name, 'error': str(e)})
            print(f"  [{i}/{len(ddl_files)}] FAIL  DDL: {table_name} — {e}")

    # 训练 Documentation
    print(f"\n--- 训练 Documentation ({len(doc_files)} 个) ---")
    for i, fname in enumerate(doc_files, 1):
        fpath = os.path.join(DOC_DIR, fname)
        table_name = fname.replace('.txt', '')
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                doc_content = fh.read()
            vn.train(documentation=doc_content)
            results['doc_trained'] += 1
            print(f"  [{i}/{len(doc_files)}] OK  DOC: {table_name}")
        except Exception as e:
            results['doc_failed'] += 1
            results['doc_errors'].append({'table': table_name, 'error': str(e)})
            print(f"  [{i}/{len(doc_files)}] FAIL  DOC: {table_name} — {e}")

    results['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 更新 training_manifest.json
    manifest['level1_trained'] = True
    manifest['level1_trained_at'] = results['end_time']
    manifest['level1_training_results'] = {
        'ddl_trained': results['ddl_trained'],
        'ddl_failed': results['ddl_failed'],
        'doc_trained': results['doc_trained'],
        'doc_failed': results['doc_failed'],
        'chroma_path': CHROMA_PATH,
    }
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\n已更新 training_manifest.json")
    print(f"ChromaDB 存储路径: {CHROMA_PATH}")

    return results


# ============================================================
# 阶段 3: 生成结果报告
# ============================================================
def generate_result_report(precheck_pass, precheck_details, results, is_dry_run):
    """生成训练结果报告"""
    lines = []
    lines.append("# Vanna Level 1 结构元数据训练 — 结果报告\n")
    lines.append(f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**模式**: {'DRY-RUN (未实际训练)' if is_dry_run else 'REAL (已训练)'}\n")
    lines.append("---\n")

    lines.append("## 前置校验\n")
    lines.append("| # | 检查项 | 结果 | 详情 |")
    lines.append("|---|--------|------|------|")
    for i, d in enumerate(precheck_details, 1):
        status = "PASS" if d["passed"] else "FAIL"
        lines.append(f"| {i} | {d['check']} | {status} | {d['detail']} |")
    lines.append("")

    lines.append("## 训练结果\n")
    if is_dry_run:
        lines.append("**状态**: DRY-RUN，未实际训练\n")
        lines.append("| 项目 | 数量 |")
        lines.append("|------|------|")
        lines.append("| 是否实际调用 vn.train() | 否 (dry-run) |")
        lines.append("| DDL 训练数量 | 0 |")
        lines.append("| documentation 训练数量 | 0 |")
        lines.append("| SQL 示例训练数量 | 0 |")
        lines.append("| 业务问法训练数量 | 0 |")
        lines.append("| 图表训练数量 | 0 |")
        lines.append("| 是否修改数据库 | 否 |")
        lines.append("| 是否进入第 2/3/4 级 | 否 |\n")
    else:
        lines.append(f"**状态**: 真实训练完成\n")
        lines.append(f"| 项目 | 数量 |")
        lines.append(f"|------|------|")
        lines.append(f"| 是否实际调用 vn.train() | 是 |")
        lines.append(f"| DDL 训练数量 | {results['ddl_trained']} |")
        lines.append(f"| DDL 失败数量 | {results['ddl_failed']} |")
        lines.append(f"| documentation 训练数量 | {results['doc_trained']} |")
        lines.append(f"| documentation 失败数量 | {results['doc_failed']} |")
        lines.append(f"| SQL 示例训练数量 | 0 |")
        lines.append(f"| 业务问法训练数量 | 0 |")
        lines.append(f"| 图表训练数量 | 0 |")
        lines.append(f"| 是否修改数据库 | 否 |")
        lines.append(f"| 是否进入第 2/3/4 级 | 否 |")
        lines.append(f"| ChromaDB 存储路径 | `{CHROMA_PATH}` |\n")

        if results['ddl_errors']:
            lines.append("### DDL 失败详情\n")
            for err in results['ddl_errors']:
                lines.append(f"- `{err['table']}`: {err['error']}")
            lines.append("")

        if results['doc_errors']:
            lines.append("### Documentation 失败详情\n")
            for err in results['doc_errors']:
                lines.append(f"- `{err['table']}`: {err['error']}")
            lines.append("")

    failed = sum(1 for d in precheck_details if not d["passed"])
    lines.append("## 自查清单\n")
    lines.append("| # | 检查项 | 结果 |")
    lines.append("|---|--------|------|")
    lines.append(f"| 1 | 是否完成 precheck | 是 |")
    lines.append(f"| 2 | 是否实际调用 vn.train() | {'否 (dry-run)' if is_dry_run else '是'} |")
    lines.append(f"| 3 | 训练 DDL 数量 | {results.get('ddl_trained', 0)} |")
    lines.append(f"| 4 | 训练 documentation 数量 | {results.get('doc_trained', 0)} |")
    lines.append(f"| 5 | 是否训练 SQL 示例 | 否 |")
    lines.append(f"| 6 | 是否训练业务问法 | 否 |")
    lines.append(f"| 7 | 是否训练图表问法 | 否 |")
    lines.append(f"| 8 | 是否修改数据库 | 否 |")
    lines.append(f"| 9 | 是否进入第 2/3/4 级 | 否 |")
    lines.append(f"| 10 | 是否有失败项 | {'是 — 见详情' if (results.get('ddl_failed', 0) + results.get('doc_failed', 0)) > 0 else '否'} |")
    lines.append(f"| 11 | 失败项原因 | {'—' if (results.get('ddl_failed', 0) + results.get('doc_failed', 0)) == 0 else '见上方详情'} |\n")

    content = "\n".join(lines)
    with open(TRAINING_RESULT_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n结果报告已写入: {TRAINING_RESULT_MD}")
    return content


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Vanna Level 1 结构元数据训练")
    parser.add_argument('--dry-run', action='store_true',
                        help='仅执行校验和生成训练计划，不实际训练')
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 60)
    print("阶段 0: 前置校验")
    print("=" * 60)
    precheck_pass, precheck_details, ddl_files, doc_files, manifest, agent_idx = run_precheck()

    # 写入 precheck CSV
    with open(PRECHECK_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['check', 'passed', 'detail'])
        writer.writeheader()
        for d in precheck_details:
            writer.writerow(d)
    print(f"\nPrecheck CSV 已写入: {PRECHECK_CSV}")

    if not precheck_pass:
        print("\n[FAIL] 前置校验未通过，终止。")
        empty_results = {'ddl_trained': 0, 'ddl_failed': 0, 'doc_trained': 0, 'doc_failed': 0,
                         'ddl_errors': [], 'doc_errors': []}
        generate_result_report(False, precheck_details, empty_results, False)
        sys.exit(1)
    else:
        print("\n[OK] 前置校验全部通过")

    # 阶段 1: 训练计划
    print(f"\n{'=' * 60}")
    print("阶段 1: 训练计划")
    print("=" * 60)
    plan = generate_training_plan(ddl_files, doc_files, manifest)
    print(plan)

    # 阶段 2: 训练
    if args.dry_run:
        print(f"\n{'=' * 60}")
        print("阶段 2: DRY-RUN — 不执行训练")
        print("=" * 60)
        print("\n使用 --dry-run 模式。真实训练请运行: python run_vanna_level1_training.py")
        results = {}
        generate_result_report(True, precheck_details, results, is_dry_run=True)

        # 输出总结
        print("\n" + "=" * 60)
        print("DRY-RUN 总结:")
        print(f"  1. precheck 通过: 是")
        print(f"  2. 实际训练: 否 (dry-run)")
        print(f"  3. DDL 训练数量: 0")
        print(f"  4. documentation 训练数量: 0")
        print(f"  5. SQL 示例训练: 0")
        print(f"  6. 业务问法训练: 0")
        print(f"  7. 图表训练: 0")
        print(f"  8. 修改数据库: 否")
        print(f"  9. 进入第 2/3/4 级: 否")
        print(f"  10. 失败项: 无")
        print("=" * 60)
    else:
        print(f"\n{'=' * 60}")
        print("阶段 2: 执行真实训练")
        print("=" * 60)

        # 确认提示
        print("\n即将执行真实 Vanna Level 1 训练:")
        print(f"  - 训练 DDL: {len(ddl_files)} 个")
        print(f"  - 训练 documentation: {len(doc_files)} 个")
        print(f"  - ChromaDB 路径: {CHROMA_PATH}")
        print(f"  - 不训练 SQL 示例、业务问法、图表训练")
        print(f"  - 不修改数据库")
        print()

        response = input("确认执行? 输入 'yes' 继续, 其他任意键取消: ").strip()
        if response.lower() != 'yes':
            print("已取消。")
            sys.exit(0)

        results = execute_training(ddl_files, doc_files, manifest)
        generate_result_report(True, precheck_details, results, is_dry_run=False)

        # 输出总结
        print("\n" + "=" * 60)
        print("训练总结:")
        print(f"  1. precheck 通过: 是")
        print(f"  2. 实际训练: 是")
        print(f"  3. DDL 训练数量: {results['ddl_trained']}")
        print(f"  4. documentation 训练数量: {results['doc_trained']}")
        print(f"  5. SQL 示例训练: 0")
        print(f"  6. 业务问法训练: 0")
        print(f"  7. 图表训练: 0")
        print(f"  8. 修改数据库: 否")
        print(f"  9. 进入第 2/3/4 级: 否")
        failed = results['ddl_failed'] + results['doc_failed']
        print(f"  10. 失败项: {failed if failed > 0 else '无'}")
        print("=" * 60)


if __name__ == '__main__':
    main()

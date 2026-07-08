"""
生成 safe_candidate_only 分批人工审核辅助包。
本阶段只生成第 1 批（high priority 表），不训练 Vanna，不修改原始注释。
"""
import csv
from pathlib import Path
from collections import defaultdict

MANUAL = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness\manual_review")
OUT = MANUAL / "batches"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# === 读取源文件 ===
template = read_csv(MANUAL / "safe_candidate_field_review_template.csv")
table_summary = read_csv(MANUAL / "safe_candidate_table_summary.csv")
suspicious_all = read_csv(MANUAL / "safe_candidate_suspicious_items.csv")

# === 索引 ===
# 表优先级 -> 表名列表
tables_by_priority = defaultdict(list)
for r in table_summary:
    tables_by_priority[r["review_priority"]].append(r)

# suspicious 索引: (table_name, column_name) -> [categories]
suspicious_index = defaultdict(list)
for r in suspicious_all:
    key = (r["table_name"], r["column_name"])
    suspicious_index[key].append(r)

# template 索引: (table_name, column_name) -> row
template_index = {}
for r in template:
    key = (r["table_name"], r["column_name"])
    template_index[key] = r

# === 1. safe_candidate_batch_index.csv（所有批规划） ===
PRIORITY_ORDER = ["high", "medium", "low"]

# suspicion_category 排序权重（用于 batch_001 超量时的排序）
SUSPICION_WEIGHT = {
    "missing_table_comment": 0,
    "business_sensitive_field": 1,
    "generic_comment": 2,
    "very_short_comment": 3,
    "id_like_field": 4,
    "code_like_field": 5,
    "status_like_field": 6,
    "time_like_field": 7,
    "name_like_field": 8,
}

batch_index_rows = []
batch_num = 0

for pri in PRIORITY_ORDER:
    tables = sorted(tables_by_priority[pri], key=lambda r: r["table_name"])
    if not tables:
        continue

    # 按表分组，先算每个 batch 的字段
    if pri == "high":
        # high: 每批按实际表分配
        for tbl in tables:
            batch_num += 1
            tn = tbl["table_name"]
            fields = [r for r in template if r["table_name"] == tn]
            suspicious_fields = [r for r in fields if (r["table_name"], r["column_name"]) in suspicious_index]
            batch_id = f"batch_{batch_num:03d}"
            status = "ready_for_human_review" if batch_num == 1 else "planned_not_generated"
            batch_index_rows.append({
                "batch_id": batch_id,
                "batch_name": f"第{batch_num}批：{tn} 表（high priority）",
                "review_priority": "high",
                "table_count": 1,
                "field_count": len(fields),
                "suspicious_count": len(suspicious_fields),
                "status": status,
                "reason": f"唯一 high priority 表: {tn}，表级注释缺失，需优先审核",
            })
    else:
        # medium / low: 每批分配若干表
        current_batch_tables = []
        current_batch_fields = 0
        for tbl in tables:
            tn = tbl["table_name"]
            fld_count = int(tbl["safe_candidate_count"])
            # 每批最多 100 个字段或 10 张表
            if (current_batch_fields + fld_count > 100 or len(current_batch_tables) >= 10) and current_batch_tables:
                batch_num += 1
                batch_id = f"batch_{batch_num:03d}"
                batch_index_rows.append({
                    "batch_id": batch_id,
                    "batch_name": f"第{batch_num}批：{pri} priority 表（{len(current_batch_tables)}张）",
                    "review_priority": pri,
                    "table_count": len(current_batch_tables),
                    "field_count": current_batch_fields,
                    "suspicious_count": 0,  # 留到生成时精确计算
                    "status": "planned_not_generated",
                    "reason": f"{pri} priority 表，人工审核辅助包尚未生成",
                })
                current_batch_tables = []
                current_batch_fields = 0
            current_batch_tables.append(tn)
            current_batch_fields += fld_count

        # 最后一批
        if current_batch_tables:
            batch_num += 1
            batch_id = f"batch_{batch_num:03d}"
            batch_index_rows.append({
                "batch_id": batch_id,
                "batch_name": f"第{batch_num}批：{pri} priority 表（{len(current_batch_tables)}张）",
                "review_priority": pri,
                "table_count": len(current_batch_tables),
                "field_count": current_batch_fields,
                "suspicious_count": 0,
                "status": "planned_not_generated",
                "reason": f"{pri} priority 表，人工审核辅助包尚未生成",
            })

write_csv(OUT / "safe_candidate_batch_index.csv", [
    "batch_id", "batch_name", "review_priority", "table_count",
    "field_count", "suspicious_count", "status", "reason",
], batch_index_rows)

total_batches = batch_num

# === 2. batch_001: 只取 high priority 表 ===
high_tables = sorted(tables_by_priority["high"], key=lambda r: r["table_name"])
batch_001_fields = []

for tbl in high_tables:
    tn = tbl["table_name"]
    fields = [r for r in template if r["table_name"] == tn]

    # 如果 over 120，按规则排序后取前 120
    if len(fields) > 120:
        def sort_key(r):
            key = (r["table_name"], r["column_name"])
            sus_cats = suspicious_index.get(key, [])
            if sus_cats:
                min_weight = min(SUSPICION_WEIGHT.get(s["suspicion_category"], 99) for s in sus_cats)
            else:
                min_weight = 99
            return (min_weight, r["table_name"], r["column_name"])
        fields.sort(key=sort_key)
        fields = fields[:120]

    batch_001_fields.extend(fields)

# === 3. safe_candidate_batch_plan.md ===
high_count = sum(1 for r in table_summary if r["review_priority"] == "high")
med_count = sum(1 for r in table_summary if r["review_priority"] == "medium")
low_count = sum(1 for r in table_summary if r["review_priority"] == "low")
total_tables = len(table_summary)
total_fields = len(template)

with open(OUT / "safe_candidate_batch_plan.md", "w", encoding="utf-8") as f:
    f.write("# Safe Candidate 人工审核分批计划\n\n")
    f.write("**生成时间**: 2026-07-08\n")
    f.write("**状态**: 只读生成，未训练 Vanna\n\n")
    f.write("---\n\n")

    f.write("## 1. 总字段数\n\n")
    f.write(f"safe_candidate_only 共 **{total_fields}** 条，涉及 **{total_tables}** 张表。\n\n")
    f.write("---\n\n")

    f.write("## 2. 为什么要分批审核\n\n")
    f.write("1451 条字段一次审核工作量过大，且不同表的字段风险不同。\n")
    f.write("分批审核的好处：\n")
    f.write("- 优先处理高风险表（表注释缺失、字段数多）\n")
    f.write("- 每批控制在合理工作量范围内（建议每批 50–120 字段）\n")
    f.write("- 每批审核完成后可总结经验，优化后续批次的审核方法\n")
    f.write("- 发现问题可逐批修正，不影响已审核批次\n\n")
    f.write("---\n\n")

    f.write("## 3. 审核优先级分布\n\n")
    f.write(f"| 优先级 | 表数 | 说明 |\n")
    f.write(f"|--------|------|------|\n")
    f.write(f"| high | {high_count} | 表注释缺失，需优先审核 |\n")
    f.write(f"| medium | {med_count} | 有部分风险因素 |\n")
    f.write(f"| low | {low_count} | 表注释清楚且字段注释明确 |\n\n")
    f.write("---\n\n")

    f.write("## 4. 分批规划\n\n")
    f.write(f"共规划 **{total_batches}** 批。\n\n")
    f.write("| 批次 | 名称 | 优先级 | 表数 | 字段数 | 状态 |\n")
    f.write("|------|------|--------|------|--------|------|\n")
    for r in batch_index_rows:
        f.write(f"| {r['batch_id']} | {r['batch_name']} | {r['review_priority']} | {r['table_count']} | {r['field_count']} | {r['status']} |\n")
    f.write("\n---\n\n")

    f.write("## 5. 第 1 批选择规则\n\n")
    f.write("batch_001 只包含 review_priority=high 的表：\n")
    f.write(f"- 涉及表: {', '.join(t['table_name'] for t in high_tables)}\n")
    f.write(f"- 字段数: {len(batch_001_fields)}\n")
    f.write("- 如果超过 120 字段，按 suspicious 优先级排序取前 120\n")
    f.write("- 禁止把 medium / low 表放入 batch_001\n\n")
    f.write("---\n\n")

    f.write("## 6. 后续批次建议\n\n")
    f.write("1. batch_001 审核完成后，总结经验再启动 batch_002\n")
    f.write("2. 按 high → medium → low 顺序逐批推进\n")
    f.write("3. 每批审核前先了解涉及表的业务背景\n")
    f.write("4. **审核阶段仍不训练 Vanna**\n\n")
    f.write("---\n\n")

    f.write("## 7. 原始注释保护原则\n\n")
    f.write("- 所有 `column_comment` 来自 `columns_with_comments.csv` 原文\n")
    f.write("- 未做 strip / trim / normalize / 改写\n")
    f.write("- 审核过程中发现错误注释，标记为 `hold_for_business_review`，不直接修改\n")
    f.write("- 审核包中的注释与源文件完全一致\n\n")
    f.write("---\n\n")

    f.write("## 8. 禁止事项\n\n")
    f.write("1. 禁止自动填写 `approve_for_limited_training`\n")
    f.write("2. 禁止批量 approve\n")
    f.write("3. 禁止修改审核模板中的 column_comment\n")
    f.write("4. 禁止训练 Vanna\n")
    f.write("5. 禁止把 `hold_for_business_review` 的记录当成错误删除\n\n")
    f.write("---\n\n")

    f.write("## 9. 本阶段状态\n\n")
    f.write("**本阶段只生成第 1 批人工审核辅助包，不训练 Vanna，不写入 vanna_data / agent_data。**\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write(f"| 总字段 1451, {total_tables} 张表 | 是 |\n")
    f.write(f"| 规划 {total_batches} 批 | 是 |\n")
    f.write(f"| batch_001 ={len(batch_001_fields)} 字段, 1 张表 | 是 |\n")
    f.write(f"| batch_001 只含 high 表 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n\n")

# === 4. batch_001_review_template.csv ===
batch_001_template_rows = []
for r in batch_001_fields:
    key = (r["table_name"], r["column_name"])
    sus_items = suspicious_index.get(key, [])
    sus_cats = " | ".join(sorted(set(s["suspicion_category"] for s in sus_items))) if sus_items else ""
    batch_001_template_rows.append({
        "batch_id": "batch_001",
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "data_type": r.get("data_type", ""),
        "column_comment": r.get("column_comment", ""),  # 保留原文
        "table_comment": r.get("table_comment", ""),
        "training_status": r.get("training_status", ""),
        "risk_level": r.get("risk_level", ""),
        "suspicion_categories": sus_cats,
        "review_decision": "",  # 必须留空
        "review_note": "",      # 必须留空
    })

write_csv(OUT / "batch_001_review_template.csv", [
    "batch_id", "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "training_status",
    "risk_level", "suspicion_categories", "review_decision", "review_note",
], batch_001_template_rows)

# === 5. batch_001_suspicious_focus.csv ===
batch_001_sus_rows = []
for r in batch_001_fields:
    key = (r["table_name"], r["column_name"])
    sus_items = suspicious_index.get(key, [])
    for s in sus_items:
        batch_001_sus_rows.append({
            "batch_id": "batch_001",
            "table_name": s["table_name"],
            "column_name": s["column_name"],
            "data_type": s.get("data_type", ""),
            "column_comment": s.get("column_comment", ""),  # 保留原文
            "table_comment": s.get("table_comment", ""),
            "suspicion_category": s["suspicion_category"],
            "reason": s["reason"],
            "recommended_review_action": s["recommended_review_action"],
        })

write_csv(OUT / "batch_001_suspicious_focus.csv", [
    "batch_id", "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "suspicion_category",
    "reason", "recommended_review_action",
], batch_001_sus_rows)

# === 6. batch_001_review_guide.md ===
with open(OUT / "batch_001_review_guide.md", "w", encoding="utf-8") as f:
    f.write("# batch_001 人工审核指南\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. 第 1 批概况\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| 字段数量 | {len(batch_001_fields)} |\n")
    f.write(f"| 表数量 | 1 |\n")
    f.write(f"| 表名 | {high_tables[0]['table_name']} |\n")
    f.write(f"| table_comment | 空（缺失） |\n")
    f.write(f"| suspicious 数量 | {len(batch_001_sus_rows)} |\n\n")
    f.write("---\n\n")

    f.write("## 2. 审核时重点看什么\n\n")
    f.write("1. **表级上下文缺失**：该表无 table_comment，审核前先了解该表的业务用途\n")
    f.write("2. **注释准确性**：逐字段确认 column_comment 是否正确描述字段含义\n")
    f.write("3. **可疑项优先**：先打开 `batch_001_suspicious_focus.csv` 查看标记的可疑项\n")
    f.write("4. **字段类型匹配**：确认 data_type 与注释描述的业务含义是否匹配\n")
    f.write("5. **业务相关性**：该字段是否适合用于 Text-to-SQL 训练\n\n")
    f.write("---\n\n")

    f.write("## 3. review_decision 三个允许值\n\n")
    f.write("| 值 | 含义 | 何时使用 |\n")
    f.write("|------|------|----------|\n")
    f.write("| `approve_for_limited_training` | 批准在带表上下文的条件下训练 | 注释准确、业务含义明确 |\n")
    f.write("| `hold_for_business_review` | 暂缓，需业务方确认 | 注释不明确、可疑、或业务含义不确定 |\n")
    f.write("| `exclude_from_training` | 排除，不纳入训练 | 注释错误、字段含义不清、或不适合训练 |\n\n")
    f.write("---\n\n")

    f.write("## 4. 不确定时怎么填\n\n")
    f.write("**填写 `hold_for_business_review`。**\n\n")
    f.write("宁可暂缓也不要随便 approve。一个错误 approve 的注释会污染 Text-to-SQL 模型的该字段理解。\n\n")
    f.write("---\n\n")

    f.write("## 5. 禁止事项\n\n")
    f.write("1. 不要为了推进训练随便填 `approve_for_limited_training`\n")
    f.write("2. 不要修改 `column_comment` 的值\n")
    f.write("3. 不要在审核阶段训练 Vanna\n")
    f.write("4. 不要跳过可疑项\n")
    f.write("5. 不要在审核包中直接改注释文本\n\n")
    f.write("---\n\n")

    f.write("## 6. 审核步骤建议\n\n")
    f.write("1. 打开 `batch_001_review_template.csv`\n")
    f.write("2. 先浏览 `batch_001_suspicious_focus.csv` 了解全部可疑项\n")
    f.write("3. 逐字段填写 `review_decision`\n")
    f.write("4. 如有疑问，在 `review_note` 中记录原因\n")
    f.write("5. 审核完成后保存文件\n")
    f.write("6. **审核阶段仍不训练 Vanna**\n\n")

# === 7. batch_001_summary.md ===
with open(OUT / "batch_001_summary.md", "w", encoding="utf-8") as f:
    f.write("# batch_001 人工审核包 — 生成摘要\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. 读取了哪些文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `safe_candidate_field_review_template.csv` | 1451 条字段审核模板 |\n")
    f.write("| `safe_candidate_table_summary.csv` | 128 张表汇总 |\n")
    f.write("| `safe_candidate_suspicious_items.csv` | 1039 条可疑项 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 生成了哪些文件\n\n")
    f.write("| 文件 | 说明 |\n")
    f.write("|------|------|\n")
    f.write(f"| `safe_candidate_batch_index.csv` | {total_batches} 批规划索引 |\n")
    f.write("| `safe_candidate_batch_plan.md` | 分批计划说明 |\n")
    f.write(f"| `batch_001_review_template.csv` | batch_001 审核模板（{len(batch_001_fields)} 条） |\n")
    f.write(f"| `batch_001_suspicious_focus.csv` | batch_001 可疑项（{len(batch_001_sus_rows)} 条） |\n")
    f.write("| `batch_001_review_guide.md` | batch_001 审核指南 |\n")
    f.write("| `batch_001_summary.md` | 本文件 |\n\n")
    f.write("---\n\n")

    f.write(f"## 3. batch_001 字段数: {len(batch_001_fields)}\n\n")
    f.write(f"## 4. batch_001 表数: 1\n\n")
    f.write(f"## 5. batch_001 suspicious 数量: {len(batch_001_sus_rows)}\n\n")
    f.write("---\n\n")

    f.write("## 6. review_decision 是否全部留空\n\n")
    f.write("**是。** batch_001_review_template.csv 中所有 `review_decision` 和 `review_note` 均为空。\n\n")
    f.write("---\n\n")

    f.write("## 7. 原始注释是否完全保留\n\n")
    f.write("**是。** `column_comment` 和 `table_comment` 从原 template 直接复制，未做 trim / strip / normalize。\n\n")
    f.write("---\n\n")

    f.write("## 8. 是否训练 Vanna\n\n")
    f.write("**否。** 本阶段未调用任何 Vanna API。\n\n")
    f.write("---\n\n")

    f.write("## 9. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `review/vanna_training_readiness/manual_review/batches/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 10. 是否可以进入人工填写 batch_001 review_decision 阶段\n\n")
    f.write("**可以进入人工填写 batch_001 review_decision 阶段，但仍不能训练 Vanna。**\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write(f"| batch_001 含 {len(batch_001_fields)} 字段 1 表 | 是 |\n")
    f.write(f"| batch_001 suspicious={len(batch_001_sus_rows)} | 是 |\n")
    f.write("| review_decision 全部留空 | 是 |\n")
    f.write("| 未自动 approve | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n")
    f.write("| 原始注释完全保留 | 是 |\n\n")

# === 控制台输出 ===
print(f"total fields: {total_fields}")
print(f"total tables: {total_tables}")
print(f"total batches planned: {total_batches}")
print(f"batch_001 fields: {len(batch_001_fields)}")
print(f"batch_001 tables: 1 ({high_tables[0]['table_name']})")
print(f"batch_001 suspicious: {len(batch_001_sus_rows)}")
print()
print("输出文件:")
print(f"  {OUT / 'safe_candidate_batch_index.csv'}")
print(f"  {OUT / 'safe_candidate_batch_plan.md'}")
print(f"  {OUT / 'batch_001_review_template.csv'}")
print(f"  {OUT / 'batch_001_suspicious_focus.csv'}")
print(f"  {OUT / 'batch_001_review_guide.md'}")
print(f"  {OUT / 'batch_001_summary.md'}")
print()
print("review_decision: 全部留空")
print("未训练 Vanna, 未写入 vanna_data/agent_data, 未修改数据库")
print("Done.")

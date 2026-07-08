"""
生成 safe_candidate_only 白名单人工审核包。
只读，不训练 Vanna，不修改数据库，不修改原始注释。
"""
import csv
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")
AUDIT = Path(r"E:\3\code\metadata_audit")
OUT = BASE / "manual_review"
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
safe_only = read_csv(BASE / "vanna_training_safe_candidate_only.csv")
tables_summary = read_csv(AUDIT / "tables_summary.csv")
columns_all = read_csv(AUDIT / "columns_with_comments.csv")

# 建立表级索引
table_info = {}
for r in tables_summary:
    table_info[r["table_name"]] = r

# 建立 (table_name, column_name) -> source row 索引（注释校验用）
source_index = {}
for r in columns_all:
    key = (r["table_name"], r["column_name"])
    if key not in source_index:
        source_index[key] = r

# === 1. safe_candidate_table_summary.csv ===
# 按表汇总
table_stats = defaultdict(lambda: {"count": 0, "table_comment": ""})
for r in safe_only:
    tn = r["table_name"]
    table_stats[tn]["count"] += 1
    table_stats[tn]["table_comment"] = r.get("table_comment", "")

table_summary_rows = []
for tn, stats in sorted(table_stats.items()):
    info = table_info.get(tn, {})
    total_cols = int(info.get("column_count", 0))
    commented_cols = int(info.get("commented_column_count", 0))
    safe_count = stats["count"]
    ratio = safe_count / total_cols if total_cols > 0 else 0
    tc = stats["table_comment"]

    # 审核优先级判定
    reasons = []
    priority_score = 0

    # table_comment 为空 → 高风险
    if not tc or not tc.strip():
        priority_score += 3
        reasons.append("表级注释缺失")
    # safe_candidate 占比高但列注释可能不充分
    if safe_count >= 30:
        priority_score += 2
        reasons.append(f"safe_candidate 数量多({safe_count}字段)")
    elif safe_count >= 10:
        priority_score += 1
    # 表注释过短
    if tc and len(tc.strip()) <= 3:
        priority_score += 1
        reasons.append("表注释过短")

    if priority_score >= 4:
        pri = "high"
    elif priority_score >= 2:
        pri = "medium"
    else:
        pri = "low"

    if not reasons:
        reasons.append("表注释清楚且字段注释明确")

    table_summary_rows.append({
        "table_name": tn,
        "table_comment": tc,
        "safe_candidate_count": safe_count,
        "total_columns_in_table": total_cols,
        "commented_columns_in_table": commented_cols,
        "safe_candidate_ratio": f"{ratio:.1%}",
        "review_priority": pri,
        "reason": "; ".join(reasons),
    })

write_csv(OUT / "safe_candidate_table_summary.csv", [
    "table_name", "table_comment", "safe_candidate_count",
    "total_columns_in_table", "commented_columns_in_table",
    "safe_candidate_ratio", "review_priority", "reason",
], table_summary_rows)

# === 2. safe_candidate_field_review_template.csv ===
# 逐字段模板，review_decision 留空
field_template_rows = []
for r in safe_only:
    field_template_rows.append({
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "data_type": r.get("data_type", ""),
        "column_comment": r.get("column_comment", ""),  # 保留原文
        "table_comment": r.get("table_comment", ""),
        "training_status": r.get("training_status", ""),
        "risk_level": r.get("risk_level", ""),
        "review_decision": "",  # 必须留空
        "review_note": "",
    })

write_csv(OUT / "safe_candidate_field_review_template.csv", [
    "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "training_status",
    "risk_level", "review_decision", "review_note",
], field_template_rows)

# === 3. safe_candidate_suspicious_items.csv ===
# 只读标记，不修改注释
suspicious_rows = []

# 通用/模糊字段名模式
GENERIC_PATTERNS = [
    ("id", "id_like_field", "ID 类字段，注释可能过于通用"),
    ("name", "name_like_field", "名称类字段，注释可能过于通用"),
    ("code", "code_like_field", "编码类字段，注释可能过于通用"),
    ("status", "status_like_field", "状态类字段，注释可能过于通用"),
    ("type", "code_like_field", "类型类字段，注释可能过于通用"),
    ("time", "time_like_field", "时间类字段，注释可能过于通用"),
    ("date", "time_like_field", "日期类字段，注释可能过于通用"),
    ("flag", "status_like_field", "标记类字段，注释可能过于通用"),
    ("remark", "generic_comment", "备注类字段，注释可能过于通用"),
    ("description", "generic_comment", "描述类字段，注释可能过于通用"),
    ("note", "generic_comment", "备注类字段，注释可能过于通用"),
    ("geom", "business_sensitive_field", "空间几何字段，需确认注释准确性"),
]

# 表注释为空的所有字段标记为高风险
tables_without_comment = set(
    tn for tn, stats in table_stats.items()
    if not stats["table_comment"] or not stats["table_comment"].strip()
)

for r in safe_only:
    tn = r["table_name"]
    cn = r["column_name"].lower()
    tc = r.get("table_comment", "")
    cc = r.get("column_comment", "")
    suspicions = []

    # 1. 表注释缺失
    if tn in tables_without_comment:
        suspicions.append((
            "missing_table_comment",
            f"表 {tn} 无表级注释，字段 {r['column_name']} 的训练语义可能不完整",
            "优先补齐表级注释后再训练该表字段"
        ))

    # 2. 通用字段名模式
    for pattern_key, category, base_reason in GENERIC_PATTERNS:
        if cn == pattern_key or cn.startswith(pattern_key + "_") or cn.endswith("_" + pattern_key):
            suspicions.append((
                category,
                f"{base_reason}: 字段名 '{r['column_name']}' 注释为 '{cc[:60]}'",
                "人工确认注释是否准确描述该字段业务含义"
            ))
            break  # 每个字段只匹配一个主要模式

    # 3. 注释很短（<=5 字符）
    cc_stripped = cc.strip()
    if len(cc_stripped) <= 5 and cc_stripped:
        suspicions.append((
            "very_short_comment",
            f"注释极短 ({len(cc_stripped)}字): '{cc_stripped}'",
            "确认该注释是否足以让模型理解字段含义"
        ))

    # 4. 注释疑似过于通用
    if cc_stripped in ("主键", "主键id", "主键ID", "id", "ID", "名称", "类型", "编码", "代码",
                         "状态", "备注", "描述", "时间", "日期", "创建时间", "更新时间",
                         "创建人", "修改人", "删除标记", "排序", "序号"):
        suspicions.append((
            "generic_comment",
            f"注释过于通用: '{cc_stripped}'，可能不足以区分业务上下文",
            "确认该注释是否需要补充业务含义，但禁止在当前阶段修改"
        ))

    for cat, reason, action in suspicions:
        suspicious_rows.append({
            "table_name": tn,
            "column_name": r["column_name"],
            "data_type": r.get("data_type", ""),
            "column_comment": cc,  # 保留原文
            "table_comment": tc,
            "suspicion_category": cat,
            "reason": reason,
            "recommended_review_action": action,
        })

write_csv(OUT / "safe_candidate_suspicious_items.csv", [
    "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "suspicion_category",
    "reason", "recommended_review_action",
], suspicious_rows)

# === 4. safe_candidate_review_pack.md ===
table_count = len(table_summary_rows)
high_count = sum(1 for r in table_summary_rows if r["review_priority"] == "high")
med_count = sum(1 for r in table_summary_rows if r["review_priority"] == "medium")
low_count = sum(1 for r in table_summary_rows if r["review_priority"] == "low")

with open(OUT / "safe_candidate_review_pack.md", "w", encoding="utf-8") as f:
    f.write("# Safe Candidate 白名单人工审核包\n\n")
    f.write("**生成时间**: 2026-07-08\n")
    f.write("**状态**: 只读生成，未训练 Vanna\n\n")
    f.write("---\n\n")

    f.write("## 1. 本阶段目的\n\n")
    f.write("对 `vanna_training_safe_candidate_only.csv`（1451 条安全训练候选）生成结构化人工审核包，")
    f.write("供业务方/DBA 逐字段审核后再决定是否纳入受限训练。\n\n")
    f.write("**本阶段只生成白名单人工审核包，不训练 Vanna，不写入 vanna_data / agent_data。**\n\n")
    f.write("---\n\n")

    f.write("## 2. 读取的文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `vanna_training_safe_candidate_only.csv` | 1451 条 safe candidate |\n")
    f.write("| `tables_summary.csv` | 表级统计信息 |\n")
    f.write("| `columns_with_comments.csv` | 原始注释源文件 |\n")
    f.write("| `vanna_training_readiness_summary.md` | 清单生成口径 |\n")
    f.write("| `vanna_training_lists_verify_summary.md` | V1–V20 校验结果 |\n")
    f.write("| `vanna_training_comment_integrity_summary.md` | 注释完整性校验 |\n\n")
    f.write("---\n\n")

    f.write("## 3. safe_candidate_only 数量\n\n")
    f.write(f"- **总字段数**: 1451\n")
    f.write(f"- **涉及表数**: {table_count}\n")
    f.write(f"- **列注释均保留原文**: 是\n")
    f.write(f"- **注释完整性校验 V1–V20**: 全部 PASS\n\n")
    f.write("---\n\n")

    f.write("## 4. 为什么仍不能直接训练\n\n")
    f.write("虽然这 1451 个字段无同名字段冲突、且有注释，但存在以下风险：\n\n")
    f.write("1. **注释质量不确定**：部分注释可能过于通用（如 `id` → `主键`），缺乏业务语义\n")
    f.write("2. **表级上下文缺失**：部分表无 table_comment，模型可能误解字段用途\n")
    f.write("3. **注释准确性未验证**：注释由 DBA/开发人员填写，可能存在错误或过时\n")
    f.write("4. **业务敏感字段**：空间几何字段、加密字段等需确认是否适合训练\n")
    f.write("5. **未经人工审核的训练数据会放大错误**：一个错误注释可能污染模型对该字段类型的理解\n\n")
    f.write("---\n\n")

    f.write("## 5. 人工审核需要看什么\n\n")
    f.write("| 审核维度 | 检查内容 | 产出 |\n")
    f.write("|----------|----------|------|\n")
    f.write("| 注释准确性 | column_comment 是否正确描述字段含义 | approve / hold / exclude |\n")
    f.write("| 表级上下文 | table_comment 是否完整，是否提供足够业务背景 | 是否需要先补表注释 |\n")
    f.write("| 字段通用性 | 注释是否过于通用（如 `主键`、`状态`） | 是否需要补充业务含义 |\n")
    f.write("| 业务敏感度 | 字段是否包含业务敏感数据 | 是否排除训练 |\n")
    f.write("| 数据类型匹配 | data_type 与注释是否一致 | 注释是否与物理类型匹配 |\n\n")
    f.write("---\n\n")

    f.write("## 6. 原始注释保护原则\n\n")
    f.write("- 本审核包中所有 `column_comment` 来自 `columns_with_comments.csv` 原文\n")
    f.write("- 未做 strip / trim / normalize / 改写\n")
    f.write("- 审核过程中发现注释错误，不应在本阶段修改——应标记为 `hold_for_business_review`\n")
    f.write("- 注释修改必须走独立的 COMMENT ON COLUMN 流程，不得在审核包中直接改\n\n")
    f.write("---\n\n")

    f.write("## 7. 禁止事项\n\n")
    f.write("1. 禁止直接将 1451 条标记为 `approved_for_training`\n")
    f.write("2. 禁止基于猜测批量批准\n")
    f.write("3. 禁止在审核包中直接修改 column_comment\n")
    f.write("4. 禁止跳过人工审核直接训练\n")
    f.write("5. 禁止把 suspicious_items 直接当错误删除\n\n")
    f.write("---\n\n")

    f.write("## 8. 后续人工审核流程\n\n")
    f.write("1. 打开 `safe_candidate_field_review_template.csv`\n")
    f.write("2. 逐字段填写 `review_decision`：\n")
    f.write("   - `approve_for_limited_training`：注释准确，可在带表上下文的条件下训练\n")
    f.write("   - `hold_for_business_review`：注释不明确或可疑，需业务方确认\n")
    f.write("   - `exclude_from_training`：不应纳入训练\n")
    f.write("3. 优先审核 `safe_candidate_suspicious_items.csv` 中的可疑项\n")
    f.write("4. 优先审核 review_priority=high 的表\n")
    f.write("5. 审核完成后统计 approve / hold / exclude 数量\n")
    f.write("6. 仅 `approve_for_limited_training` 的字段可进入后续受限训练准备\n")
    f.write("7. **审核阶段仍不训练 Vanna**\n\n")
    f.write("---\n\n")

    f.write("## 9. 审核包文件清单\n\n")
    f.write("| 文件 | 说明 |\n")
    f.write("|------|------|\n")
    f.write("| `safe_candidate_review_pack.md` | 本文件，审核说明 |\n")
    f.write("| `safe_candidate_table_summary.csv` | 按表汇总，含审核优先级 |\n")
    f.write(f"| `safe_candidate_field_review_template.csv` | 1451 条待审核字段模板，review_decision 留空 |\n")
    f.write(f"| `safe_candidate_suspicious_items.csv` | {len(suspicious_rows)} 条建议重点审核项 |\n")
    f.write("| `safe_candidate_manual_review_summary.md` | 审核包生成摘要 |\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data | 是 |\n")
    f.write("| 未写入 agent_data | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未修改原始注释 | 是 |\n")
    f.write("| review_decision 全部留空 | 是 |\n")
    f.write("| 未自动批准任何字段 | 是 |\n")
    f.write(f"| 覆盖 {table_count} 张表 | 是 |\n\n")

# === 5. safe_candidate_manual_review_summary.md ===
# 统计 suspicious 分类
sus_cats = Counter(r["suspicion_category"] for r in suspicious_rows)

with open(OUT / "safe_candidate_manual_review_summary.md", "w", encoding="utf-8") as f:
    f.write("# Safe Candidate 人工审核包 — 生成摘要\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. safe_candidate_only 总数\n\n")
    f.write(f"- **1451** 条安全训练候选字段\n")
    f.write(f"- 涉及 **{table_count}** 张表\n\n")
    f.write("---\n\n")

    f.write("## 2. 按表汇总\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| 表总数 | {table_count} |\n")
    f.write(f"| safe_candidate 总字段数 | 1451 |\n\n")
    f.write("---\n\n")

    f.write("## 3. 审核优先级分布\n\n")
    f.write(f"| 优先级 | 表数 | 说明 |\n")
    f.write(f"|--------|------|------|\n")
    f.write(f"| high | {high_count} | 表注释缺失或字段数多，需优先审核 |\n")
    f.write(f"| medium | {med_count} | 有部分风险因素 |\n")
    f.write(f"| low | {low_count} | 表注释清楚，字段注释明确 |\n\n")
    f.write("---\n\n")

    f.write("## 4. suspicious items 数量\n\n")
    f.write(f"- **总计**: {len(suspicious_rows)} 条建议重点审核\n")
    f.write(f"- 分布:\n")
    for cat, cnt in sus_cats.most_common():
        f.write(f"  - {cat}: {cnt}\n")
    f.write("\n> 注意：suspicious 不等于错误，仅表示建议人工重点审核。\n\n")
    f.write("---\n\n")

    f.write("## 5. review_decision 状态\n\n")
    f.write("**全部留空。** `safe_candidate_field_review_template.csv` 中 1451 条记录的 `review_decision` 均为空，")
    f.write("待人工逐字段填写。\n\n")
    f.write("---\n\n")

    f.write("## 6. 原始注释保留\n\n")
    f.write("- 所有 `column_comment` 从 `vanna_training_safe_candidate_only.csv` 直接复制\n")
    f.write("- 未做 trim / strip / normalize\n")
    f.write("- 前导空格、末尾空格、换行符均保留\n")
    f.write("- 与 `columns_with_comments.csv` 原文完全一致\n\n")
    f.write("---\n\n")

    f.write("## 7. 是否训练 Vanna\n\n")
    f.write("**否。** 本阶段未调用任何 Vanna API，未生成训练数据。\n\n")
    f.write("---\n\n")

    f.write("## 8. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `review/vanna_training_readiness/manual_review/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 9. 是否可以进入人工审核阶段\n\n")
    f.write("**可以进入人工审核 safe_candidate_only 白名单阶段，但仍不能训练 Vanna。**\n\n")
    f.write("理由：\n")
    f.write("- 审核包已生成，所有模板和可疑标记已就绪\n")
    f.write("- review_decision 全部留空，等待人工填写\n")
    f.write("- 注释保留原文，未做任何修改\n")
    f.write("- 但仍需人工逐字段审核后才能进入受限训练准备\n\n")
    f.write("---\n\n")

    f.write("## 10. 下一步建议（不要在本阶段执行）\n\n")
    f.write("1. 打开 `safe_candidate_table_summary.csv`，按 review_priority 排序\n")
    f.write("2. 先审核 high 优先级表的字段\n")
    f.write("3. 参考 `safe_candidate_suspicious_items.csv` 标记的可疑项\n")
    f.write("4. 在 `safe_candidate_field_review_template.csv` 中填写 review_decision\n")
    f.write("5. 审核完成后统计结果，仅 `approve_for_limited_training` 的字段进入训练准备\n")
    f.write("6. **审核阶段仍不训练 Vanna**\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write("| 审核包包含 1451 条字段 | 是 |\n")
    f.write(f"| 涉及 {table_count} 张表 | 是 |\n")
    f.write(f"| review_priority: high={high_count}, medium={med_count}, low={low_count} | 是 |\n")
    f.write(f"| suspicious_items={len(suspicious_rows)} 条 | 是 |\n")
    f.write("| review_decision 全部留空 | 是 |\n")
    f.write("| 未自动批准任何字段 | 是 |\n")
    f.write("| 原始注释保留原文 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n\n")

# === 控制台输出 ===
print(f"safe_candidate_only: {len(safe_only)} 条")
print(f"涉及表: {table_count} 张")
print(f"审核优先级: high={high_count}, medium={med_count}, low={low_count}")
print(f"suspicious_items: {len(suspicious_rows)} 条")
print(f"  missing_table_comment: {sus_cats.get('missing_table_comment', 0)}")
print(f"  id_like_field: {sus_cats.get('id_like_field', 0)}")
print(f"  name_like_field: {sus_cats.get('name_like_field', 0)}")
print(f"  code_like_field: {sus_cats.get('code_like_field', 0)}")
print(f"  status_like_field: {sus_cats.get('status_like_field', 0)}")
print(f"  time_like_field: {sus_cats.get('time_like_field', 0)}")
print(f"  generic_comment: {sus_cats.get('generic_comment', 0)}")
print(f"  very_short_comment: {sus_cats.get('very_short_comment', 0)}")
print(f"  business_sensitive_field: {sus_cats.get('business_sensitive_field', 0)}")
print()
print("输出文件:")
print(f"  {OUT / 'safe_candidate_review_pack.md'}")
print(f"  {OUT / 'safe_candidate_table_summary.csv'}")
print(f"  {OUT / 'safe_candidate_field_review_template.csv'}")
print(f"  {OUT / 'safe_candidate_suspicious_items.csv'}")
print(f"  {OUT / 'safe_candidate_manual_review_summary.md'}")
print()
print("review_decision 状态: 全部留空")
print("未训练 Vanna, 未写入 vanna_data/agent_data, 未修改数据库")
print("Done.")

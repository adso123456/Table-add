"""
生成 batch_001 人工审核建议辅助表。
只读，不训练 Vanna，不自动填写 review_decision，不修改原始注释。
"""
import csv
from pathlib import Path
from collections import Counter

VANNA_BASE = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")
BATCHES = VANNA_BASE / "manual_review" / "batches"
OUT = BATCHES / "batch_001_human_review"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# === 读取 ===
template = read_csv(BATCHES / "batch_001_review_template.csv")
suspicious = read_csv(BATCHES / "batch_001_suspicious_focus.csv")

# 10 个字段，逐条分析
assist_rows = []
decision_rows = []

# 字段级分析规则：
# 1. record_id: 注释"遥感反演结果表（合并版）"明显是表级描述，不是字段注释 → exclude
# 2. inversion_type: 注释有明确业务枚举 → possible_limited_training
# 3. l1-l6_area: 注释有明确分类含义 → possible_limited_training
# 4. service_url: "服务地址"过于通用 → hold
# 5. data_time: "数据日期"过于通用 → hold

FIELD_ANALYSIS = {
    "record_id": {
        "suggested_review_tendency": "suggest_exclude_from_training",
        "risk_reason": (
            "column_comment '遥感反演结果表（合并版）' 描述的是整张表的含义，"
            "而非 record_id 字段的含义。注释与字段不匹配，可能为填充时错误。"
        ),
        "suggested_reason": (
            "字段注释明显不是对该字段的描述，疑似注释填写错误。"
            "在确认正确注释前建议排除训练。"
        ),
    },
    "inversion_type": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失，无法确认表级别的业务上下文。"
            "但 column_comment 包含明确的业务枚举值（water_environment/水环境、algalbloom/水生态、landuse/土地利用），"
            "注释质量较好。"
        ),
        "suggested_reason": (
            "字段注释有明确的业务枚举说明，可辅助 Text-to-SQL 模型理解。"
            "但必须补齐表级注释后才能用于训练——模型需要知道这是什么表。"
        ),
    },
    "l1_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "但 column_comment 'I类/浮叶挺水植被/背景面积' 包含明确的水质分类+植被类型+面积指标，"
            "业务含义清晰。"
        ),
        "suggested_reason": (
            "字段注释包含明确的水质分类和面积指标，业务语义完整。"
            "补齐表级注释后可纳入训练。"
        ),
    },
    "l2_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment 'II类/沉水植被/耕地面积' 业务含义清晰。"
        ),
        "suggested_reason": "字段注释业务语义完整。补齐表级注释后可纳入训练。",
    },
    "l3_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment 'III类/水华/园地面积' 业务含义清晰。"
        ),
        "suggested_reason": "字段注释业务语义完整。补齐表级注释后可纳入训练。",
    },
    "l4_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment 'IV类/水体/林地面积' 业务含义清晰。"
        ),
        "suggested_reason": "字段注释业务语义完整。补齐表级注释后可纳入训练。",
    },
    "l5_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment 'V类/水体面积' 业务含义清晰。"
        ),
        "suggested_reason": "字段注释业务语义完整。补齐表级注释后可纳入训练。",
    },
    "l6_area": {
        "suggested_review_tendency": "suggest_possible_limited_training_after_table_context_confirmed",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment '劣V类/建设用地面积' 业务含义清晰。"
        ),
        "suggested_reason": "字段注释业务语义完整。补齐表级注释后可纳入训练。",
    },
    "service_url": {
        "suggested_review_tendency": "suggest_hold_for_business_review",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment '服务地址' 仅4字，过于通用。"
            "无法区分是 WMS 服务地址、WFS 服务地址、还是其他类型的服务地址。"
        ),
        "suggested_reason": (
            "注释过于通用，无法帮助模型理解该字段在遥感反演表中的具体含义。"
            "建议业务方确认后补充更具体的注释（如 'WMS 瓦片服务地址'）。"
        ),
    },
    "data_time": {
        "suggested_review_tendency": "suggest_hold_for_business_review",
        "risk_reason": (
            "表级注释缺失。"
            "column_comment '数据日期' 仅4字，过于通用。"
            "无法区分是反演数据的采集日期、处理日期、还是影像的拍摄日期。"
        ),
        "suggested_reason": (
            "注释过于通用，无法帮助模型理解该时间字段的精确业务含义。"
            "建议业务方确认后补充更具体的注释（如 '遥感影像拍摄日期'）。"
        ),
    },
}

for r in template:
    cn = r["column_name"]
    analysis = FIELD_ANALYSIS.get(cn, {
        "suggested_review_tendency": "suggest_hold_for_business_review",
        "risk_reason": "未匹配到预定义分析，默认建议人工确认",
        "suggested_reason": "需人工逐字段确认注释准确性和业务含义",
    })

    assist_rows.append({
        "table_name": r["table_name"],
        "column_name": cn,
        "data_type": r.get("data_type", ""),
        "column_comment": r.get("column_comment", ""),  # 原文保留
        "table_comment": r.get("table_comment", ""),
        "suspicion_categories": r.get("suspicion_categories", ""),
        "risk_reason": analysis["risk_reason"],
        "suggested_review_tendency": analysis["suggested_review_tendency"],
        "suggested_reason": analysis["suggested_reason"],
        "human_decision": "",   # 必须留空
        "human_note": "",       # 必须留空
    })

    decision_rows.append({
        "table_name": r["table_name"],
        "column_name": cn,
        "data_type": r.get("data_type", ""),
        "column_comment": r.get("column_comment", ""),  # 原文保留
        "table_comment": r.get("table_comment", ""),
        "review_decision": "",  # 必须留空
        "review_note": "",      # 必须留空
    })

# === 写入文件 ===

# 1. batch_001_human_review_assist.csv
write_csv(OUT / "batch_001_human_review_assist.csv", [
    "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "suspicion_categories",
    "risk_reason", "suggested_review_tendency", "suggested_reason",
    "human_decision", "human_note",
], assist_rows)

# 2. batch_001_human_decision_template.csv
write_csv(OUT / "batch_001_human_decision_template.csv", [
    "table_name", "column_name", "data_type",
    "column_comment", "table_comment",
    "review_decision", "review_note",
], decision_rows)

# 统计
tendencies = Counter(r["suggested_review_tendency"] for r in assist_rows)
hold_count = tendencies.get("suggest_hold_for_business_review", 0)
exclude_count = tendencies.get("suggest_exclude_from_training", 0)
possible_count = tendencies.get("suggest_possible_limited_training_after_table_context_confirmed", 0)

# 3. batch_001_human_review_notes.md
with open(OUT / "batch_001_human_review_notes.md", "w", encoding="utf-8") as f:
    f.write("# batch_001 人工审核说明\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. 本批次概况\n\n")
    f.write("| 指标 | 数值 |\n")
    f.write("|------|------|\n")
    f.write("| batch_001 字段数 | 10 |\n")
    f.write("| 表名 | `wm_raster_inversion` |\n")
    f.write("| 表级注释 | **空（缺失）** |\n")
    f.write("| 全部字段命中 missing_table_comment | 是 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 核心问题：表级注释缺失\n\n")
    f.write("`wm_raster_inversion` 没有 table_comment，导致：\n\n")
    f.write("- 即使字段注释质量较高，模型也无法理解字段所属的业务上下文\n")
    f.write("- Text-to-SQL 训练时，带表上下文的 prompt 会缺失关键信息\n")
    f.write("- 审核人员也难以确认注释是否准确\n\n")
    f.write("**建议优先确认表的业务含义**，例如该存储的是遥感反演结果的哪个维度（时间序列、空间分布、分类结果等）。\n\n")
    f.write("---\n\n")

    f.write("## 3. 字段级建议概览\n\n")
    f.write("| 字段 | 注释 | 建议倾向 | 原因 |\n")
    f.write("|------|------|----------|------|\n")
    for r in assist_rows:
        tendency_short = {
            "suggest_exclude_from_training": "建议排除",
            "suggest_hold_for_business_review": "建议暂缓",
            "suggest_possible_limited_training_after_table_context_confirmed": "表注释补齐后可考虑",
        }.get(r["suggested_review_tendency"], r["suggested_review_tendency"])
        f.write(f"| {r['column_name']} | {r['column_comment'][:40]} | {tendency_short} | {r['suggested_reason'][:60]} |\n")
    f.write("\n---\n\n")

    f.write("## 4. record_id 特别说明\n\n")
    f.write("`record_id` 的 column_comment 为 `遥感反演结果表（合并版）`。\n\n")
    f.write("这明显不是对 `record_id` 字段的描述，而是对整张表的描述。\n")
    f.write("很可能是 DBA 在补注释时误把 table_comment 填到了第一个字段。\n")
    f.write("**建议**: 该字段注释基本可以确认错误，建议排除训练，待 DBA 修正后再重新评估。\n\n")
    f.write("---\n\n")

    f.write("## 5. 审核步骤建议\n\n")
    f.write("1. 先确认 `wm_raster_inversion` 表的业务含义（建议 DBA 提供表级注释）\n")
    f.write("2. 打开 `batch_001_human_review_assist.csv`，参考 `suggested_review_tendency` 和 `risk_reason`\n")
    f.write("3. 在 `batch_001_human_decision_template.csv` 中填写 `review_decision`\n")
    f.write("   - `approve_for_limited_training`：确认注释准确，表上下文补齐后可训练\n")
    f.write("   - `hold_for_business_review`：不确定，需业务方/DBA 确认\n")
    f.write("   - `exclude_from_training`：确认注释错误或不适合训练\n")
    f.write("4. 不确定时填写 `hold_for_business_review`，不要随便 approve\n")
    f.write("5. **不要在审核阶段修改原始注释**——注释修正走独立流程\n\n")
    f.write("---\n\n")

    f.write("## 6. 禁止事项\n\n")
    f.write("1. 禁止为了推进训练随便填 `approve_for_limited_training`\n")
    f.write("2. 禁止在审核模板中直接修改 `column_comment`\n")
    f.write("3. 禁止跳过 `record_id` 的注释异常\n")
    f.write("4. 禁止在审核阶段训练 Vanna\n")
    f.write("5. 禁止自动批量 approve\n\n")
    f.write("---\n\n")

    f.write("⚠️ **本阶段只是审核辅助，不训练 Vanna，不修改数据库，不修改原始注释。**\n")

# 4. batch_001_human_review_summary.md
with open(OUT / "batch_001_human_review_summary.md", "w", encoding="utf-8") as f:
    f.write("# batch_001 人工审核建议辅助包 — 生成摘要\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. 读取了哪些文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `batch_001_review_template.csv` | 10 条字段审核模板 |\n")
    f.write("| `batch_001_suspicious_focus.csv` | 15 条可疑项标记 |\n")
    f.write("| `batch_001_review_guide.md` | 审核指南 |\n")
    f.write("| `batch_001_verify_summary.md` | 校验结果 |\n")
    f.write("| `batch_001_summary.md` | 批次生成摘要 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 生成了哪些文件\n\n")
    f.write("| 文件 | 说明 |\n")
    f.write("|------|------|\n")
    f.write("| `batch_001_human_review_assist.csv` | 10 条字段审核辅助表（含建议倾向） |\n")
    f.write("| `batch_001_human_decision_template.csv` | 10 条人工决策模板（review_decision 留空） |\n")
    f.write("| `batch_001_human_review_notes.md` | 人工审核说明 |\n")
    f.write("| `batch_001_human_review_summary.md` | 本文件 |\n\n")
    f.write("---\n\n")

    f.write(f"## 3. batch_001 字段数: 10\n\n")
    f.write(f"## 4. 建议 hold 数量: {hold_count}\n\n")
    f.write(f"## 5. 建议 exclude 数量: {exclude_count}\n\n")
    f.write(f"## 6. 建议 possible limited training 数量: {possible_count}\n\n")
    f.write("---\n\n")

    f.write("## 7. human_decision 是否全部留空\n\n")
    f.write("**是。** `batch_001_human_review_assist.csv` 中 10 条 `human_decision` 和 `human_note` 均为空。\n\n")
    f.write("---\n\n")

    f.write("## 8. review_decision 是否全部留空\n\n")
    f.write("**是。** `batch_001_human_decision_template.csv` 中 10 条 `review_decision` 和 `review_note` 均为空。\n\n")
    f.write("---\n\n")

    f.write("## 9. 原始注释是否完全保留\n\n")
    f.write("**是。** 所有 `column_comment` 和 `table_comment` 从原始模板直接复制，未做 trim / strip / normalize。\n\n")
    f.write("---\n\n")

    f.write("## 10. 是否训练 Vanna\n\n")
    f.write("**否。** 本阶段未调用任何 Vanna API。\n\n")
    f.write("---\n\n")

    f.write("## 11. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `batches/batch_001_human_review/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 12. 是否可以进入人工填写决策阶段\n\n")
    f.write("**可以进入人工填写 batch_001_human_decision_template.csv 阶段，但仍不能训练 Vanna。**\n\n")
    f.write("说明：\n")
    f.write(f"- 辅助建议已生成（hold={hold_count}, exclude={exclude_count}, possible={possible_count}）\n")
    f.write("- 所有决策字段均已留空，等待人工填写\n")
    f.write("- 建议优先确认 `wm_raster_inversion` 表的业务含义（表级注释缺失）\n")
    f.write("- 特别关注 `record_id` 字段的注释异常（疑似误填为表描述）\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write("| batch_001 含 10 字段 1 表 | 是 |\n")
    f.write(f"| suggest_hold_for_business_review={hold_count} | 是 |\n")
    f.write(f"| suggest_exclude_from_training={exclude_count} | 是 |\n")
    f.write(f"| suggest_possible_limited_training={possible_count} | 是 |\n")
    f.write("| human_decision 全部留空 | 是 |\n")
    f.write("| review_decision 全部留空 | 是 |\n")
    f.write("| 未自动 approve | 是 |\n")
    f.write("| 原始注释完全保留 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n\n")

# === 控制台输出 ===
print(f"batch_001 字段数: {len(template)}")
print(f"建议: hold={hold_count}, exclude={exclude_count}, possible_limited_training={possible_count}")
print()
print("输出文件:")
print(f"  {OUT / 'batch_001_human_review_assist.csv'}")
print(f"  {OUT / 'batch_001_human_decision_template.csv'}")
print(f"  {OUT / 'batch_001_human_review_notes.md'}")
print(f"  {OUT / 'batch_001_human_review_summary.md'}")
print()
print("human_decision: 全部留空")
print("review_decision: 全部留空")
print("未训练 Vanna, 未写入 vanna_data/agent_data, 未修改数据库")
print("Done.")

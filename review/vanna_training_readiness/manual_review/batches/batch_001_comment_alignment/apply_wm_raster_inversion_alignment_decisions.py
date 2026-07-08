"""
写入 wm_raster_inversion 注释对齐人工确认结果。
只写确认结论，不生成 SQL，不修改数据库，不训练 Vanna。
"""
import csv
from pathlib import Path

BATCHES = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness\manual_review\batches")
OUT = BATCHES / "batch_001_comment_alignment"


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# 读取原模板，保留 current_comment 和 candidate_comment 不变
decision = read_csv(OUT / "wm_raster_inversion_comment_alignment_decision_template.csv")

# 人工确认结果
DECISIONS = {
    ("table", "wm_raster_inversion", ""): {
        "human_decision": "approve",
        "human_note": "人工确认：wm_raster_inversion 表示遥感反演结果表（合并版）",
    },
    ("column", "wm_raster_inversion", "record_id"): {
        "human_decision": "approve",
        "human_note": "人工确认：record_id 表示遥感反演结果记录ID；原注释疑似表级描述误填到字段注释",
    },
}

# 填入确认结果
for r in decision:
    key = (r["object_type"], r["table_name"], r["column_name"])
    dec = DECISIONS.get(key)
    if dec:
        r["human_decision"] = dec["human_decision"]
        r["human_note"] = dec["human_note"]

# 写入更新后的 decision_template
write_csv(OUT / "wm_raster_inversion_comment_alignment_decision_template.csv", [
    "object_type", "table_name", "column_name",
    "current_comment", "candidate_comment",
    "human_decision", "human_note",
], decision)

# 统计
approve_count = sum(1 for r in decision if r["human_decision"] == "approve")
hold_count = sum(1 for r in decision if r["human_decision"] == "hold_for_business_review")
reject_count = sum(1 for r in decision if r["human_decision"] == "reject")

# 生成 decision_summary.md
with open(OUT / "wm_raster_inversion_comment_alignment_decision_summary.md", "w", encoding="utf-8") as f:
    f.write("# wm_raster_inversion 注释对齐 — 人工确认决策总结\n\n")
    f.write("**人工确认时间**: 2026-07-08\n")
    f.write("**状态**: 已写入人工确认结果，未生成 SQL，未训练 Vanna\n\n")
    f.write("---\n\n")

    f.write("## 1. 读取了哪些文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `wm_raster_inversion_comment_alignment_candidate.csv` | 2 条注释对齐候选 |\n")
    f.write("| `wm_raster_inversion_comment_alignment_decision_template.csv` | 决策模板 |\n")
    f.write("| `wm_raster_inversion_comment_alignment_notes.md` | 人工确认说明 |\n")
    f.write("| `wm_raster_inversion_comment_alignment_summary.md` | 候选包生成摘要 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 决策结果\n\n")
    f.write(f"| 决策 | 数量 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| approve | {approve_count} |\n")
    f.write(f"| hold_for_business_review | {hold_count} |\n")
    f.write(f"| reject | {reject_count} |\n\n")
    f.write("---\n\n")

    f.write("## 3. 批准的表级注释候选\n\n")
    f.write("| 表 | 当前注释 | 候选注释 | 决策 |\n")
    f.write("|------|----------|----------|------|\n")
    for r in decision:
        if r["object_type"] == "table":
            f.write(f"| {r['table_name']} | (空) | {r['candidate_comment']} | {r['human_decision']} |\n")
    f.write("\n说明：`wm_raster_inversion` 表级注释已确认，后续可作为表上下文用于 Text-to-SQL 训练。\n\n")
    f.write("---\n\n")

    f.write("## 4. 批准的字段注释修正候选\n\n")
    f.write("| 表 | 字段 | 当前注释 | 候选注释 | 决策 |\n")
    f.write("|------|------|----------|----------|------|\n")
    for r in decision:
        if r["object_type"] == "column":
            f.write(f"| {r['table_name']} | {r['column_name']} | {r['current_comment']} | {r['candidate_comment']} | {r['human_decision']} |\n")
    f.write("\n说明：`record_id` 原注释 `遥感反演结果表（合并版）` 确认为表级描述误填，修正为字段级注释。\n\n")
    f.write("---\n\n")

    f.write("## 5. 是否生成 SQL\n\n")
    f.write("**否。** 本阶段仅写入人工确认结果，未生成任何 SQL 草案。\n\n")
    f.write("---\n\n")

    f.write("## 6. 是否执行 SQL\n\n")
    f.write("**否。** 未连接数据库，未执行任何 DDL。\n\n")
    f.write("---\n\n")

    f.write("## 7. 是否修改数据库\n\n")
    f.write("**否。** 数据库中的 `wm_raster_inversion` 表注释和 `record_id` 字段注释尚未修改。\n\n")
    f.write("---\n\n")

    f.write("## 8. 是否训练 Vanna\n\n")
    f.write("**否。** 未调用任何 Vanna API。\n\n")
    f.write("---\n\n")

    f.write("## 9. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `batches/batch_001_comment_alignment/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 10. 是否可以进入 SQL 草案生成阶段\n\n")
    f.write("**可以进入 wm_raster_inversion 注释对齐 SQL 草案生成阶段，但仍不能执行 SQL，不能训练 Vanna。**\n\n")
    f.write("说明：\n")
    f.write("- 2 条候选已全部人工 approve\n")
    f.write("- candidate_comment 和 current_comment 保持不变\n")
    f.write("- 后续阶段：生成 COMMENT ON TABLE / COMMENT ON COLUMN 草案供 DBA 审核执行\n")
    f.write("- SQL 草案仍需人工检查后才能执行\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write(f"| approve={approve_count}, hold={hold_count}, reject={reject_count} | 是 |\n")
    f.write("| candidate_comment 未被修改 | 是 |\n")
    f.write("| current_comment 未被修改 | 是 |\n")
    f.write("| 未生成 SQL | 是 |\n")
    f.write("| 未执行 SQL | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n\n")

print(f"decision_template 行数: {len(decision)}")
print(f"approve={approve_count}, hold={hold_count}, reject={reject_count}")
print(f"candidate_comment 保持不变: 是")
print(f"current_comment 保持不变: 是")
print(f"未生成 SQL, 未执行 SQL, 未修改数据库, 未训练 Vanna")
print("Done.")

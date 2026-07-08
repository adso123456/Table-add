"""
生成 wm_raster_inversion 注释对齐候选包。
只读，不执行 SQL，不修改数据库，不训练 Vanna。
本阶段只生成候选供人工确认，不自动批准任何注释修改。
"""
import csv
from pathlib import Path

VANNA_BASE = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")
BATCHES = VANNA_BASE / "manual_review" / "batches"
OUT = BATCHES / "batch_001_comment_alignment"
OUT.mkdir(parents=True, exist_ok=True)


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# === 候选定义 ===

# 候选 1: 表级注释补齐
table_candidate = {
    "object_type": "table",
    "table_name": "wm_raster_inversion",
    "column_name": "",
    "current_comment": "",
    "candidate_comment": "遥感反演结果表（合并版）",
    "evidence": (
        "record_id 当前字段注释为'遥感反演结果表（合并版）'，"
        "语义上更像是对整张表的描述而非对 record_id 字段的描述。"
        "推测 DBA 补注释时误将表级描述填入了第一个字段。"
        "batch_001 人工审核已确认表级注释缺失是高风险项。"
    ),
    "risk_level": "low",
    "recommendation": "human_confirm_required",
    "human_decision": "",
    "human_note": "",
}

# 候选 2: record_id 字段注释修正
column_candidate = {
    "object_type": "column",
    "table_name": "wm_raster_inversion",
    "column_name": "record_id",
    "current_comment": "遥感反演结果表（合并版）",
    "candidate_comment": "遥感反演结果记录ID",
    "evidence": (
        "record_id 数据类型为 bigint，字段名包含 'id'，符合记录标识字段特征。"
        "当前注释'遥感反演结果表（合并版）'疑似整表描述误填。"
        "如果表级注释确认采用'遥感反演结果表（合并版）'，"
        "则 record_id 应修正为记录标识类字段注释。"
    ),
    "risk_level": "medium",
    "recommendation": "human_confirm_required",
    "human_decision": "",
    "human_note": "",
}

candidates = [table_candidate, column_candidate]

# === 1. wm_raster_inversion_comment_alignment_candidate.csv ===
write_csv(OUT / "wm_raster_inversion_comment_alignment_candidate.csv", [
    "object_type", "table_name", "column_name",
    "current_comment", "candidate_comment",
    "evidence", "risk_level", "recommendation",
    "human_decision", "human_note",
], candidates)

# === 2. wm_raster_inversion_comment_alignment_decision_template.csv ===
decision_rows = []
for c in candidates:
    decision_rows.append({
        "object_type": c["object_type"],
        "table_name": c["table_name"],
        "column_name": c["column_name"],
        "current_comment": c["current_comment"],
        "candidate_comment": c["candidate_comment"],
        "human_decision": "",
        "human_note": "",
    })

write_csv(OUT / "wm_raster_inversion_comment_alignment_decision_template.csv", [
    "object_type", "table_name", "column_name",
    "current_comment", "candidate_comment",
    "human_decision", "human_note",
], decision_rows)

# === 3. wm_raster_inversion_comment_alignment_notes.md ===
with open(OUT / "wm_raster_inversion_comment_alignment_notes.md", "w", encoding="utf-8") as f:
    f.write("# wm_raster_inversion 注释对齐候选 — 人工确认说明\n\n")
    f.write("**生成时间**: 2026-07-08\n")
    f.write("**状态**: 只读生成候选，未执行 SQL，未训练 Vanna\n\n")
    f.write("---\n\n")

    f.write("## 1. 为什么要补表级注释\n\n")
    f.write("`wm_raster_inversion` 当前无 table_comment，导致：\n\n")
    f.write("- 审核人员无法确认表的业务用途\n")
    f.write("- Text-to-SQL 模型训练时缺少关键的上下文信息\n")
    f.write("- 10 个字段全部命中 `missing_table_comment` 风险标记\n\n")
    f.write("补齐表级注释是后续所有工作的前提。\n\n")
    f.write("---\n\n")

    f.write("## 2. 为什么 record_id 当前注释疑似错误\n\n")
    f.write("| 现象 | 说明 |\n")
    f.write("|------|------|\n")
    f.write("| 当前注释 | `遥感反演结果表（合并版）` |\n")
    f.write("| 字段名 | `record_id` |\n")
    f.write("| 数据类型 | `bigint` |\n\n")
    f.write("该注释语义上描述的是整张表，而非 `record_id` 这个字段。\n")
    f.write("推测 DBA 在前序注释补齐流程中，误将表级描述填入了该表的第一个字段。\n")
    f.write("`record_id` 本身应是记录标识字段，建议修正为 `遥感反演结果记录ID`。\n\n")
    f.write("**但这条修正必须先经人工确认，不能自动执行。**\n\n")
    f.write("---\n\n")

    f.write("## 3. 为什么不能直接修改已有注释\n\n")
    f.write("原始注释保护原则要求：\n\n")
    f.write("1. 已有注释默认视为事实源\n")
    f.write("2. 修改已有注释 = 覆盖事实源，必须有人工确认的证据链\n")
    f.write("3. 不能因为'看起来像错误'就直接改——可能是我们理解有偏差\n")
    f.write("4. COMMENT ON COLUMN 是 DDL，执行后不可回退（除非有备份）\n")
    f.write("5. 本阶段只生成候选，人工确认后才进入 SQL 草案阶段\n\n")
    f.write("---\n\n")

    f.write("## 4. 为什么 service_url / data_time 不应编造更具体含义\n\n")
    f.write("| 字段 | 当前注释 | 为什么不编造 |\n")
    f.write("|------|----------|-------------|\n")
    f.write("| `service_url` | `服务地址` | 无法确认是 WMS/WFS/TMS/其他协议，编造含义反而引入错误 |\n")
    f.write("| `data_time` | `数据日期` | 无法确认是采集日期/处理日期/影像拍摄日期，编造含义反而引入错误 |\n\n")
    f.write("**原则**：不确定时不编造。等到有业务方确认的真实信息后再补充。\n\n")
    f.write("---\n\n")

    f.write("## 5. 其他字段（inversion_type、l1_area–l6_area）\n\n")
    f.write("这些字段的注释质量较高，包含明确的业务分类/枚举值，暂不提出修改候选。\n")
    f.write("它们的训练可用性取决于表级注释是否补齐。\n\n")
    f.write("---\n\n")

    f.write("## 6. 人工确认后才能进入 SQL 草案阶段\n\n")
    f.write("当前阶段不生成 SQL。人工确认后，后续阶段才会：\n\n")
    f.write("1. 生成 COMMENT ON TABLE / COMMENT ON COLUMN 草案\n")
    f.write("2. 通过人工执行检查清单确认\n")
    f.write("3. 由 DBA 在数据库执行\n\n")
    f.write("---\n\n")

    f.write("## 7. 本阶段状态\n\n")
    f.write("**本阶段不执行 SQL，不训练 Vanna，不写入 vanna_data / agent_data。**\n\n")
    f.write("---\n\n")

    f.write("## 人工确认步骤\n\n")
    f.write("1. 打开 `wm_raster_inversion_comment_alignment_candidate.csv`\n")
    f.write("2. 逐条审查候选注释是否合理\n")
    f.write("3. 在 `wm_raster_inversion_comment_alignment_decision_template.csv` 中填写 `human_decision`：\n")
    f.write("   - `approve`：确认候选注释正确\n")
    f.write("   - `hold_for_business_review`：不确定，需业务方/DBA 进一步确认\n")
    f.write("   - `reject`：候选注释不合理，应放弃\n")
    f.write("4. 不确定时填写 `hold_for_business_review`\n")
    f.write("5. 审批通过后才能进入 SQL 草案生成阶段\n\n")
    f.write("⚠️ **本阶段只是候选，不执行 SQL，不修改数据库，不训练 Vanna。**\n")

# === 4. wm_raster_inversion_comment_alignment_summary.md ===
with open(OUT / "wm_raster_inversion_comment_alignment_summary.md", "w", encoding="utf-8") as f:
    f.write("# wm_raster_inversion 注释对齐候选包 — 生成摘要\n\n")
    f.write("**生成时间**: 2026-07-08\n\n")
    f.write("---\n\n")

    f.write("## 1. 读取了哪些文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `batch_001_review_template.csv` | 10 条字段审核模板 |\n")
    f.write("| `batch_001_suspicious_focus.csv` | 15 条可疑项 |\n")
    f.write("| `batch_001_human_review_assist.csv` | 建议倾向（确认 record_id 注释异常） |\n")
    f.write("| `batch_001_human_decision_template.csv` | 决策模板（参考） |\n")
    f.write("| `batch_001_human_review_summary.md` | 审核包摘要 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 生成了哪些文件\n\n")
    f.write("| 文件 | 说明 |\n")
    f.write("|------|------|\n")
    f.write("| `wm_raster_inversion_comment_alignment_candidate.csv` | 2 条注释对齐候选（含证据和风险评估） |\n")
    f.write("| `wm_raster_inversion_comment_alignment_decision_template.csv` | 2 条人工决策模板（human_decision 留空） |\n")
    f.write("| `wm_raster_inversion_comment_alignment_notes.md` | 人工确认说明 |\n")
    f.write("| `wm_raster_inversion_comment_alignment_summary.md` | 本文件 |\n\n")
    f.write("---\n\n")

    f.write("## 3. 表级注释候选数量\n\n")
    f.write("**1** 条：`wm_raster_inversion` 表注释候选 → `遥感反演结果表（合并版）`\n\n")
    f.write("## 4. 字段注释修正候选数量\n\n")
    f.write("**1** 条：`record_id` 注释候选 → `遥感反演结果记录ID`\n\n")
    f.write("## 5. 其他字段是否保持不变\n\n")
    f.write("**是。** `inversion_type`、`l1_area`–`l6_area`、`service_url`、`data_time` 共 9 个字段的注释不提出修改候选。\n")
    f.write("其中 `inversion_type` + `l1_area`–`l6_area` 注释质量较好，`service_url` 和 `data_time` 证据不足不编造。\n\n")
    f.write("---\n\n")

    f.write("## 6. human_decision 是否全部留空\n\n")
    f.write("**是。** 两个模板中所有 `human_decision` 和 `human_note` 均为空。\n\n")
    f.write("---\n\n")

    f.write("## 7. 是否修改数据库\n\n")
    f.write("**否。** 未连接数据库，未执行任何 DDL。\n\n")
    f.write("## 8. 是否执行 SQL\n\n")
    f.write("**否。** 本阶段未生成任何 SQL。\n\n")
    f.write("## 9. 是否训练 Vanna\n\n")
    f.write("**否。** 未调用任何 Vanna API。\n\n")
    f.write("## 10. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `batches/batch_001_comment_alignment/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 11. 是否可以进入人工确认阶段\n\n")
    f.write("**可以进入人工确认 wm_raster_inversion 注释对齐候选阶段，但仍不能执行 SQL，不能训练 Vanna。**\n\n")
    f.write("说明：\n")
    f.write("- 2 条候选已生成，含证据和风险评估\n")
    f.write("- 所有 human_decision 已留空，等待人工填写\n")
    f.write("- 候选涉及修改已有注释（record_id），必须单独人工确认\n")
    f.write("- 其他 9 个字段注释保持不变\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write("| 表级注释候选 1 条 | 是 |\n")
    f.write("| 字段注释修正候选 1 条 | 是 |\n")
    f.write("| 其他 9 字段不变 | 是 |\n")
    f.write("| human_decision 全部留空 | 是 |\n")
    f.write("| 未执行 SQL | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未改造已有注释 | 是 |\n")
    f.write("| 未编造 service_url/data_time 含义 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n\n")

print("表级注释候选: 1 条")
print("字段注释修正候选: 1 条")
print("其他 9 字段: 保持不变")
print()
print("human_decision: 全部留空")
print("未执行 SQL, 未训练 Vanna, 未写入 vanna_data/agent_data")
print("Done.")

"""
生成 wm_raster_inversion 注释对齐 SQL 草案。
只生成草案，不执行 SQL，不修改数据库，不训练 Vanna。
"""
import csv
from pathlib import Path

BATCHES = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness\manual_review\batches")
ALIGN = BATCHES / "batch_001_comment_alignment"
OUT = ALIGN / "sql_draft"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


decision = read_csv(ALIGN / "wm_raster_inversion_comment_alignment_decision_template.csv")

approved = [r for r in decision if r["human_decision"] == "approve"]

# === 1. SQL 草案文件 ===
sql_lines = [
    "-- wm_raster_inversion 注释对齐 SQL 草案",
    "-- 生成时间: 2026-07-08",
    "-- 状态: 草案，待人工执行前最终确认，未执行",
    "-- 警告: 本文件为草案，不能直接执行。执行前需人工检查。",
    "",
]

for r in approved:
    if r["object_type"] == "table":
        sql_lines.append(
            f'COMMENT ON TABLE public."{r["table_name"]}" IS '
            f"'{r['candidate_comment']}';"
        )
    elif r["object_type"] == "column":
        sql_lines.append(
            f'COMMENT ON COLUMN public."{r["table_name"]}"."{r["column_name"]}" IS '
            f"'{r['candidate_comment']}';"
        )

sql_lines.append("")

with open(OUT / "wm_raster_inversion_comment_alignment_draft.sql", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(sql_lines))

# === 2. manifest.csv ===
manifest_rows = []
for r in approved:
    stmt_type = "COMMENT ON TABLE" if r["object_type"] == "table" else "COMMENT ON COLUMN"
    note = ""
    if r["object_type"] == "table":
        note = "新建表级注释，原表无注释"
    elif r["object_type"] == "column":
        note = "修正字段注释：原注释疑似表级描述误填，人工确认修正为字段级注释"

    manifest_rows.append({
        "object_type": r["object_type"],
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "current_comment": r["current_comment"],
        "candidate_comment": r["candidate_comment"],
        "human_decision": r["human_decision"],
        "sql_generated": "yes",
        "sql_statement_type": stmt_type,
        "risk_level": "low" if r["object_type"] == "table" else "medium",
        "note": note,
    })

write_csv(OUT / "wm_raster_inversion_comment_alignment_manifest.csv", [
    "object_type", "table_name", "column_name",
    "current_comment", "candidate_comment",
    "human_decision", "sql_generated", "sql_statement_type",
    "risk_level", "note",
], manifest_rows)

# === 3. sql_summary.md ===
table_count = sum(1 for r in approved if r["object_type"] == "table")
col_count = sum(1 for r in approved if r["object_type"] == "column")

with open(OUT / "wm_raster_inversion_comment_alignment_sql_summary.md", "w", encoding="utf-8") as f:
    f.write("# wm_raster_inversion 注释对齐 — SQL 草案生成摘要\n\n")
    f.write("**生成时间**: 2026-07-08\n")
    f.write("**状态**: SQL 草案已生成，未执行，未训练 Vanna\n\n")
    f.write("---\n\n")

    f.write("## 1. 读取了哪些文件\n\n")
    f.write("| 文件 | 用途 |\n")
    f.write("|------|------|\n")
    f.write("| `wm_raster_inversion_comment_alignment_decision_template.csv` | 2 条已 approve 的决策 |\n")
    f.write("| `wm_raster_inversion_comment_alignment_decision_summary.md` | 人工确认决策总结 |\n\n")
    f.write("---\n\n")

    f.write("## 2. 生成 SQL 草案数量\n\n")
    f.write(f"**{len(approved)}** 条\n\n")
    f.write(f"| 类型 | 数量 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| COMMENT ON TABLE | {table_count} |\n")
    f.write(f"| COMMENT ON COLUMN | {col_count} |\n\n")
    f.write("---\n\n")

    f.write("## 3. SQL 草案内容\n\n")
    f.write("```sql\n")
    for line in sql_lines:
        f.write(line + "\n")
    f.write("```\n\n")
    f.write("---\n\n")

    f.write("## 4. 是否执行 SQL\n\n")
    f.write("**否。** 本阶段仅生成草案，未连接数据库，未执行任何 SQL。\n\n")
    f.write("---\n\n")

    f.write("## 5. 是否训练 Vanna\n\n")
    f.write("**否。** 未调用任何 Vanna API。\n\n")
    f.write("---\n\n")

    f.write("## 6. 是否写入 vanna_data / agent_data\n\n")
    f.write("**否。** 所有输出在 `batches/batch_001_comment_alignment/sql_draft/` 下。\n\n")
    f.write("---\n\n")

    f.write("## 7. 是否可以进入 SQL 执行前最终确认阶段\n\n")
    f.write("**可以进入 SQL 执行前最终确认阶段，但仍不能执行 SQL，不能训练 Vanna。**\n\n")
    f.write("说明：\n")
    f.write("- 2 条 SQL 草案已生成\n")
    f.write("- 2 条均为 COMMENT ON 语句（无数据修改风险）\n")
    f.write("- 执行前仍需人工检查：表名、字段名、schema 是否正确\n")
    f.write("- 建议在非生产环境先验证后再上生产\n\n")
    f.write("---\n\n")

    f.write("## 关键确认\n\n")
    f.write("| 确认项 | 结果 |\n")
    f.write("|--------|------|\n")
    f.write(f"| SQL 草案 {len(approved)} 条 | 是 |\n")
    f.write(f"| COMMENT ON TABLE {table_count} 条 | 是 |\n")
    f.write(f"| COMMENT ON COLUMN {col_count} 条 | 是 |\n")
    f.write("| sql_generated=yes | 是 |\n")
    f.write("| 未执行 SQL | 是 |\n")
    f.write("| 未修改数据库 | 是 |\n")
    f.write("| 未训练 Vanna | 是 |\n")
    f.write("| 未写入 vanna_data / agent_data | 是 |\n")
    f.write("| 未修改项目代码 | 是 |\n\n")

print(f"SQL 草案: {len(approved)} 条")
print(f"  COMMENT ON TABLE: {table_count}")
print(f"  COMMENT ON COLUMN: {col_count}")
print(f"未执行 SQL, 未训练 Vanna, 未写入 vanna_data/agent_data")
print("Done.")

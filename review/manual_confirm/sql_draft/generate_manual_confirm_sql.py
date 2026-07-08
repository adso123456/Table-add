"""
为 3 条人工确认 approve 字段生成 COMMENT ON COLUMN SQL 草案。
不连接数据库，不执行 SQL。
"""
import csv
import os
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
CONFIRM_DIR = os.path.join(REVIEW_DIR, "manual_confirm")
SQL_DIR = os.path.join(CONFIRM_DIR, "sql_draft")
os.makedirs(SQL_DIR, exist_ok=True)

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(subdir, fname):
    with open(os.path.join(subdir, fname), encoding="utf-8-sig") as f:
        lines = [l for l in f if not l.strip().startswith("#")]
    # re-parse from string
    reader = csv.DictReader(lines)
    return list(reader)


# ── 加载源文件 ────────────────────────────────────────────────────────
decision_tmpl = read_csv(CONFIRM_DIR, "manual_confirm_decision_template.csv")
columns_all = read_csv(DIR, "columns_with_comments.csv")
ts_rows = read_csv(DIR, "tables_summary.csv")

# ── 过滤 approve ──────────────────────────────────────────────────────
approved_decisions = [r for r in decision_tmpl if r["human_decision"].strip() == "approve"]
assert len(approved_decisions) == 3, f"Expected 3 approve, got {len(approved_decisions)}"

ts_set = set(r["table_name"] for r in ts_rows)
cc_index = {}
for c in columns_all:
    cc_index[(c["table_name"], c["column_name"])] = c

# ── 生成 ──────────────────────────────────────────────────────────────
manifest = []
sql_lines = []

sql_header = f"""-- ============================================================================
-- DRAFT ONLY — COMMENT ON COLUMN SQL 草案（人工确认版）
-- ============================================================================
-- 本文件仅为人工确认后的 COMMENT ON COLUMN SQL 草案，尚未执行。
-- 来源：manual_confirm_decision_template.csv
-- 生成时间：{now_str}
--
-- 禁止未经最终人工确认直接在生产库执行。
-- ============================================================================
"""
sql_lines.append(sql_header.rstrip())

for d in approved_decisions:
    tn = d["table_name"]
    cn = d["column_name"]
    proposed = d["proposed_comment"]
    decision = d["human_decision"].strip()
    note = d.get("human_note", "")

    # 检查 target table
    if tn not in ts_set:
        manifest.append({
            "table_schema": "public", "table_name": tn, "column_name": cn,
            "proposed_comment": proposed, "human_decision": decision,
            "human_note": note, "current_comment": "N/A",
            "sql_generated": False, "status": "skipped_not_in_main_table",
            "reason": f"目标表 {tn} 不在 tables_summary 主表集合",
        })
        continue

    # 检查 target column
    ckey = (tn, cn)
    ccol = cc_index.get(ckey)
    if not ccol:
        manifest.append({
            "table_schema": "public", "table_name": tn, "column_name": cn,
            "proposed_comment": proposed, "human_decision": decision,
            "human_note": note, "current_comment": "COLUMN_NOT_FOUND",
            "sql_generated": False, "status": "skipped_missing_target_column",
            "reason": "目标字段在 columns_with_comments.csv 中不存在",
        })
        continue

    current = (ccol.get("column_comment") or "").strip()
    if current:
        manifest.append({
            "table_schema": "public", "table_name": tn, "column_name": cn,
            "proposed_comment": proposed, "human_decision": decision,
            "human_note": note, "current_comment": current,
            "sql_generated": False, "status": "skipped_already_has_comment",
            "reason": f"字段已有注释: '{current}'",
        })
        continue

    # 生成 SQL
    escaped = proposed.replace("'", "''")
    sql = f'COMMENT ON COLUMN public."{tn}"."{cn}" IS \'{escaped}\';'

    sql_lines.append(f"-- #: {tn}.{cn}")
    sql_lines.append(f"-- Human confirmed: {note}")
    sql_lines.append(sql)
    sql_lines.append("")

    manifest.append({
        "table_schema": "public", "table_name": tn, "column_name": cn,
        "proposed_comment": proposed, "human_decision": decision,
        "human_note": note, "current_comment": "",
        "sql_generated": True, "status": "generated",
        "reason": "",
    })

# ── 写入 SQL 文件 ─────────────────────────────────────────────────────
sql_path = os.path.join(SQL_DIR, "manual_confirm_comment_on_columns_draft.sql")
with open(sql_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines) + "\n")
print(f"manual_confirm_comment_on_columns_draft.sql generated")

# ── 写入 manifest ─────────────────────────────────────────────────────
manifest_fields = [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "human_decision", "human_note", "current_comment",
    "sql_generated", "status", "reason"
]
manifest_path = os.path.join(SQL_DIR, "manual_confirm_comment_manifest.csv")
with open(manifest_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=manifest_fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(manifest)
print(f"manual_confirm_comment_manifest.csv - {len(manifest)} rows")

# ── 统计 ──────────────────────────────────────────────────────────────
generated = [m for m in manifest if m["status"] == "generated"]
skipped = [m for m in manifest if m["status"] != "generated"]
gen_count = len(generated)
skip_count = len(skipped)

# forbidden keywords check
sql_body = "\n".join(l for l in sql_lines if not l.strip().startswith("--"))
forbidden = ["UPDATE ", "DELETE ", "INSERT ", "DROP ", "ALTER ", "CREATE ", "BEGIN ", "COMMIT "]
import re
found_kw = [kw for kw in forbidden if re.search(r'\b' + kw.strip() + r'\b', sql_body, re.IGNORECASE)]
sql_clean = len(found_kw) == 0

# ── 写入 summary ──────────────────────────────────────────────────────
gen_details = "\n".join(
    f"| {m['table_name']}.{m['column_name']} | {m['proposed_comment']} | {m['human_note']} |"
    for m in generated
)
skip_details = "\n".join(
    f"| {m['table_name']}.{m['column_name']} | {m['status']} | {m['reason']} |"
    for m in skipped
) if skipped else "| (无) | | |"

summary_md = f"""# 人工确认 COMMENT ON COLUMN SQL 草案报告

**生成时间**: {now_str}
**来源**: manual_confirm_decision_template.csv

---

## 读取文件

| 文件 | 用途 |
|------|------|
| manual_confirm_decision_template.csv | 人工确认结果（3 approve） |
| columns_with_comments.csv | 确认缺注释状态 |
| tables_summary.csv | 确认主表集合 |

---

## 统计

| 指标 | 数值 |
|------|------|
| 人工确认 approve 总数 | {len(approved_decisions)} |
| 生成 SQL 条数 | **{gen_count}** |
| skipped 数量 | {skip_count} |

## 生成 SQL 清单

| 字段 | 注释 | 人工备注 |
|------|------|----------|
{gen_details}

## skipped 明细

{skip_details}

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 只包含人工确认 approve 字段 | 是 |
| 不包含 keep_manual | 是 |
| 不包含 rejected | 是 |
| 不包含其他 missing 字段 | 是 |
| 不包含 UPDATE / DELETE / INSERT / DROP / ALTER / CREATE | {'是' if sql_clean else '否: ' + str(found_kw)} |
| 不包含 BEGIN / COMMIT | 是 |
| 未连接数据库 | 是 |
| 未执行 SQL | 是 |
| 未修改数据库 | 是 |
| 未训练 Vanna | 是 |

---

## SQL 草案文件

- SQL: `review/manual_confirm/sql_draft/manual_confirm_comment_on_columns_draft.sql`
- Manifest: `review/manual_confirm/sql_draft/manual_confirm_comment_manifest.csv`

---

## 下一步建议

进入执行前最终确认阶段，确认后可按与 approved 13 条相同的 Docker 方式受控执行。不要在本阶段执行。

---

本阶段未连接数据库，未执行 SQL，未修改数据库，未训练 Vanna。
"""

summary_path = os.path.join(SQL_DIR, "manual_confirm_sql_summary.md")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_md)
print("manual_confirm_sql_summary.md generated")

# ── 终端输出 ──────────────────────────────────────────────────────────
print(f"\n=== Generation result ===")
print(f"Approved decisions: {len(approved_decisions)}")
print(f"SQL generated: {gen_count}")
print(f"Skipped: {skip_count}")
print(f"SQL clean (no forbidden keywords): {sql_clean}")
if not sql_clean:
    print(f"  Found: {found_kw}")

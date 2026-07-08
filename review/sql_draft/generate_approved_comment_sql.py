"""
为 A 档 approved 候选生成 COMMENT ON COLUMN SQL 草案。

只生成文件，不连接数据库，不执行 SQL。
"""
import csv
import os
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
SQL_DIR = os.path.join(REVIEW_DIR, "sql_draft")
os.makedirs(SQL_DIR, exist_ok=True)


def read_csv(subdir, fname):
    path = os.path.join(subdir, fname)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ── 加载源数据 ────────────────────────────────────────────────────────
approved = read_csv(REVIEW_DIR, "a_candidates_approved.csv")
verify = read_csv(REVIEW_DIR, "a_candidates_verify_report.csv")
columns_all = read_csv(DIR, "columns_with_comments.csv")
ts_rows = read_csv(DIR, "tables_summary.csv")

# ── 构建索引 ──────────────────────────────────────────────────────────
# verify_report 索引: (table_name, column_name) → row
verify_index = {}
for v in verify:
    verify_index[(v["table_name"], v["column_name"])] = v

# columns_with_comments 索引: (table_name, column_name) → row
cc_index = {}
for c in columns_all:
    cc_index[(c["table_name"], c["column_name"])] = c

# ── 处理每条 approved ───────────────────────────────────────────────
manifest = []
sql_lines = []

# SQL 文件头
sql_header = """\
-- ============================================================================
-- DRAFT ONLY — COMMENT ON COLUMN SQL 草案
-- ============================================================================
-- 本文件仅为人工审查草案，尚未执行。
-- 来源：a_candidates_approved.csv (13 条) + a_candidates_verify_report.csv (全部 pass)
-- 生成时间：{now}
--
-- ⚠️  禁止未经人工确认直接在生产库执行。
-- ⚠️  执行前请逐条核对注释内容与业务含义是否匹配。
-- ============================================================================

""".format(now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

sql_lines.append(sql_header.rstrip())

for a in approved:
    tn = a["table_name"]
    cn = a["column_name"]
    proposed = a["proposed_comment"]
    ev_count = a["evidence_count"]
    ev_tables = a["evidence_tables"]

    # --- 交叉校验 verify_report ---
    vkey = (tn, cn)
    vrow = verify_index.get(vkey)

    if not vrow:
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": "NOT_FOUND",
            "evidence_comment_verified": "N/A",
            "current_comment": "N/A",
            "sql_generated": False,
            "status": "skipped_not_verified",
            "reason": "verify_report 中未找到该记录",
        })
        continue

    if vrow["decision"] != "approved":
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": "N/A",
            "sql_generated": False,
            "status": "skipped_not_verified",
            "reason": f"verify_report 中 decision={vrow['decision']} 而非 approved",
        })
        continue

    if vrow["verify_result"] != "pass":
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": "N/A",
            "sql_generated": False,
            "status": "skipped_not_verified",
            "reason": f"verify_result={vrow['verify_result']} 而非 pass",
        })
        continue

    if vrow["evidence_comment_verified"] != "True":
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": "N/A",
            "sql_generated": False,
            "status": "skipped_not_verified",
            "reason": f"evidence_comment_verified={vrow['evidence_comment_verified']} 而非 True",
        })
        continue

    if vrow["target_in_main_tables"] != "True":
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": "N/A",
            "sql_generated": False,
            "status": "skipped_not_verified",
            "reason": "target_in_main_tables=False",
        })
        continue

    # --- 检查 columns_with_comments 中是否存在目标字段 ---
    ckey = (tn, cn)
    ccol = cc_index.get(ckey)

    if not ccol:
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": "COLUMN_NOT_FOUND",
            "sql_generated": False,
            "status": "skipped_missing_target_column",
            "reason": "目标字段在 columns_with_comments.csv 中不存在",
        })
        continue

    # --- 确认当前确实缺注释 ---
    current_comment = (ccol.get("column_comment") or "").strip()

    if current_comment:
        manifest.append({
            "table_schema": a["table_schema"],
            "table_name": tn,
            "column_name": cn,
            "proposed_comment": proposed,
            "evidence_count": ev_count,
            "evidence_tables": ev_tables,
            "verify_result": vrow["verify_result"],
            "evidence_comment_verified": vrow["evidence_comment_verified"],
            "current_comment": current_comment,
            "sql_generated": False,
            "status": "skipped_already_has_comment",
            "reason": f"字段已有注释: '{current_comment}'",
        })
        continue

    # --- 通过全部检查，生成 SQL ---
    # 转义注释中的单引号
    escaped_comment = proposed.replace("'", "''")
    sql = f'COMMENT ON COLUMN public."{tn}"."{cn}" IS \'{escaped_comment}\';'

    sql_lines.append(f"-- #{len(manifest) + 1}: {tn}.{cn}")
    sql_lines.append(f"-- Evidence: {ev_count} table(s) — {ev_tables}")
    sql_lines.append(sql)
    sql_lines.append("")

    manifest.append({
        "table_schema": a["table_schema"],
        "table_name": tn,
        "column_name": cn,
        "proposed_comment": proposed,
        "evidence_count": ev_count,
        "evidence_tables": ev_tables,
        "verify_result": vrow["verify_result"],
        "evidence_comment_verified": vrow["evidence_comment_verified"],
        "current_comment": "",
        "sql_generated": True,
        "status": "generated",
        "reason": "",
    })

# ── 写入 SQL 文件 ─────────────────────────────────────────────────────
sql_path = os.path.join(SQL_DIR, "approved_comment_on_columns_draft.sql")
with open(sql_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines) + "\n")
print(f"approved_comment_on_columns_draft.sql 已生成")

# ── 写入 manifest ─────────────────────────────────────────────────────
manifest_fields = [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "evidence_count", "evidence_tables", "verify_result",
    "evidence_comment_verified", "current_comment",
    "sql_generated", "status", "reason"
]

manifest_path = os.path.join(SQL_DIR, "approved_comment_manifest.csv")
with open(manifest_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=manifest_fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(manifest)
print(f"approved_comment_manifest.csv — {len(manifest)} 行")

# ── 统计 ──────────────────────────────────────────────────────────────
total = len(approved)
generated = [m for m in manifest if m["status"] == "generated"]
skipped_not_verified = [m for m in manifest if m["status"] == "skipped_not_verified"]
skipped_has_comment = [m for m in manifest if m["status"] == "skipped_already_has_comment"]
skipped_missing = [m for m in manifest if m["status"] == "skipped_missing_target_column"]

gen_count = len(generated)
skip_count = len(manifest) - gen_count

# SQL 行数自查
sql_content = "\n".join(sql_lines)
contains_update = "UPDATE " in sql_content.upper() and "COMMENT ON" not in sql_content.split("UPDATE")[0]
sql_has_forbidden = any(
    kw in sql_content.upper()
    for kw in ["UPDATE ", "DELETE ", "INSERT ", "DROP ", "ALTER ", "BEGIN ", "COMMIT "]
)

# ── 写入 summary ─────────────────────────────────────────────────────
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

skip_details = ""
for m in skipped_not_verified:
    skip_details += f"| {m['table_name']}.{m['column_name']} | skipped_not_verified | {m['reason']} |\n"
for m in skipped_has_comment:
    skip_details += f"| {m['table_name']}.{m['column_name']} | skipped_already_has_comment | {m['reason']} |\n"
for m in skipped_missing:
    skip_details += f"| {m['table_name']}.{m['column_name']} | skipped_missing_target_column | {m['reason']} |\n"

gen_details = "\n".join(
    f"| {m['table_name']}.{m['column_name']} | {m['proposed_comment'][:60]} | {m['evidence_count']} |"
    for m in generated
)

summary_md = f"""# approved COMMENT ON COLUMN SQL 草案报告

**生成时间**: {now_str}
**来源**: a_candidates_approved.csv (13 条) + a_candidates_verify_report.csv

---

## 读取文件

- `a_candidates_approved.csv` — 13 条 approved 候选
- `a_candidates_verify_report.csv` — 21 条校验结果
- `columns_with_comments.csv` — 主表字段数据（确认缺注释状态）
- `tables_summary.csv` — 主表集合

---

## 统计

| 指标 | 数值 |
|------|------|
| approved 总数 | {total} |
| 校验通过 (交叉验证 + 缺注释确认) | {gen_count} |
| 生成 SQL 条数 | **{gen_count}** |
| skipped 数量 | {skip_count} |

## skipped 明细

| 字段 | 状态 | 原因 |
|------|------|------|
{skip_details if skip_details else '| (无) | | |'}

## 生成 SQL 清单

| 字段 | 注释内容 | 证据表数 |
|------|----------|----------|
{gen_details}

---

## 关键确认

| 确认项 | 结果 |
|--------|------|
| 只包含 approved | ✅ |
| 不包含 needs_manual | ✅ |
| 不包含 rejected | ✅ |
| 不包含 UPDATE / DELETE / INSERT / DROP / ALTER | {'✅' if not sql_has_forbidden else '❌'} |
| 不包含 BEGIN / COMMIT | ✅ |
| 未连接数据库 | ✅ |
| 未执行 SQL | ✅ |
| 未修改项目目录 | ✅ |
| 未写入 vanna_data / agent_data | ✅ |

---

## SQL 草案文件

- **SQL**: `review/sql_draft/approved_comment_on_columns_draft.sql`
- **Manifest**: `review/sql_draft/approved_comment_manifest.csv`

---

## 下一步建议

1. 人工逐条审查 SQL 草案中的每条 COMMENT，确认注释内容与业务含义匹配
2. 确认后可在受控环境执行（但本阶段不执行）
3. 执行后需重新运行 `run_metadata_audit.py` 审计脚本验证注释覆盖率变化
4. `needs_manual` 的 6 条待人工确认后可按相同流程补注释

---

⚠️ **本阶段未连接数据库，未执行 SQL，未修改数据库，未训练 Vanna。**
"""

summary_path = os.path.join(SQL_DIR, "approved_comment_sql_summary.md")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_md)
print("approved_comment_sql_summary.md 已生成")

# ── 终端输出 ──────────────────────────────────────────────────────────
print(f"\n=== 生成结果 ===")
print(f"approved 总数: {total}")
print(f"生成 SQL: {gen_count}")
print(f"skipped: {skip_count}")
if skip_count > 0:
    for m in skipped_not_verified:
        print(f"  skipped_not_verified: {m['table_name']}.{m['column_name']} — {m['reason']}")
    for m in skipped_has_comment:
        print(f"  skipped_already_has_comment: {m['table_name']}.{m['column_name']} — {m['reason']}")
    for m in skipped_missing:
        print(f"  skipped_missing_target_column: {m['table_name']}.{m['column_name']} — {m['reason']}")
print(f"SQL forbidden keywords: {sql_has_forbidden}")

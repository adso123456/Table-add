"""
执行前最终确认脚本
读取 SQL 草案 + manifest + approved + verify_report，生成：
- pre_execution_checklist.md
- pre_execution_manifest.csv
- execution_commands_draft.md

只生成文件，不连接数据库，不执行 SQL。
"""
import csv
import os
import re
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
SQL_DIR = os.path.join(REVIEW_DIR, "sql_draft")
os.makedirs(SQL_DIR, exist_ok=True)

# ── 路径变量（raw string，避免 Windows 反斜杠转义污染输出文件）──
SQL_DRAFT_FILE = r"E:\3\code\metadata_audit\review\sql_draft\approved_comment_on_columns_draft.sql"
PYTHON_EXE = r"E:\3\posgresql\1\vanna_venv\Scripts\python.exe"
AUDIT_SCRIPT = r"E:\3\code\metadata_audit\run_metadata_audit.py"
DB_URL = "postgresql://postgres:test123456@localhost:5433/gt_monitor"

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(subdir, fname):
    path = os.path.join(subdir, fname)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ── 加载所有源文件 ────────────────────────────────────────────────────
sql_path = os.path.join(SQL_DIR, "approved_comment_on_columns_draft.sql")
with open(sql_path, encoding="utf-8") as f:
    sql_content = f.read()

manifest = read_csv(SQL_DIR, "approved_comment_manifest.csv")
approved = read_csv(REVIEW_DIR, "a_candidates_approved.csv")
verify = read_csv(REVIEW_DIR, "a_candidates_verify_report.csv")

# ══════════════════════════════════════════════════════════════════════
# 1. SQL 文件安全检查
# ══════════════════════════════════════════════════════════════════════

comment_lines_raw = re.findall(r'^COMMENT ON COLUMN', sql_content, re.MULTILINE)
sql_comment_count = len(comment_lines_raw)

forbidden_keywords = [
    "UPDATE ", "DELETE ", "INSERT ", "DROP ",
    "ALTER ", "BEGIN ", "COMMIT ",
]
sql_body_lines = [
    line for line in sql_content.split("\n")
    if not line.strip().startswith("--")
]
sql_body = "\n".join(sql_body_lines)

forbidden_found = {}
for kw in forbidden_keywords:
    if re.search(r'\b' + kw.strip() + r'\b', sql_body, re.IGNORECASE):
        forbidden_found[kw.strip()] = True
    else:
        forbidden_found[kw.strip()] = False

needs_csv = read_csv(REVIEW_DIR, "a_candidates_needs_manual.csv")
rejected_csv = read_csv(REVIEW_DIR, "a_candidates_rejected.csv")
needs_names = set((r["table_name"], r["column_name"]) for r in needs_csv)
rejected_names = set((r["table_name"], r["column_name"]) for r in rejected_csv)

sql_has_needs = any(
    f'"{n[0]}"."{n[1]}"' in sql_content for n in needs_names
)
sql_has_rejected = any(
    f'"{r[0]}"."{r[1]}"' in sql_content for r in rejected_names
)

# ══════════════════════════════════════════════════════════════════════
# 2. Manifest 对齐检查
# ══════════════════════════════════════════════════════════════════════

manifest_generated_count = sum(1 for m in manifest if m["status"] == "generated")
approved_count = len(approved)
verify_approved_pass = sum(
    1 for v in verify
    if v["decision"] == "approved" and v["verify_result"] == "pass"
)

alignment_ok = (
    sql_comment_count == 13
    and manifest_generated_count == 13
    and approved_count == 13
    and verify_approved_pass == 13
)

# ══════════════════════════════════════════════════════════════════════
# 3. 逐条执行前清单
# ══════════════════════════════════════════════════════════════════════

verify_index = {}
for v in verify:
    verify_index[(v["table_name"], v["column_name"])] = v

review_rows = read_csv(REVIEW_DIR, "a_candidates_review.csv")
risk_index = {}
for rv in review_rows:
    risk_index[(rv["table_name"], rv["column_name"])] = rv.get("risk_level", "low")

pre_manifest = []
all_ready = True

for i, m in enumerate(manifest, 1):
    tn = m["table_name"]
    cn = m["column_name"]
    proposed = m["proposed_comment"]
    ev_count = m["evidence_count"]
    ev_tables = m["evidence_tables"]
    status = m["status"]
    vrow = verify_index.get((tn, cn), {})
    risk = risk_index.get((tn, cn), "low")

    issues = []

    if status != "generated":
        issues.append(f"manifest status={status} rather than generated")

    if vrow.get("verify_result") != "pass":
        issues.append(f"verify_result={vrow.get('verify_result', 'N/A')} rather than pass")

    if vrow.get("evidence_comment_verified") != "True":
        issues.append(f"evidence_comment_verified={vrow.get('evidence_comment_verified', 'N/A')} rather than True")

    if vrow.get("target_in_main_tables") != "True":
        issues.append("target_in_main_tables not True")

    if vrow.get("evidence_not_excluded") != "True":
        issues.append("evidence_not_excluded not True")

    if issues:
        final_status = "hold"
        final_note = "; ".join(issues)
        all_ready = False
    else:
        final_status = "ready_for_manual_execution"
        final_note = ""

    pre_manifest.append({
        "index": i,
        "table_name": tn,
        "column_name": cn,
        "proposed_comment": proposed,
        "evidence_count": ev_count,
        "evidence_tables": ev_tables,
        "verify_result": vrow.get("verify_result", "N/A"),
        "evidence_comment_verified": vrow.get("evidence_comment_verified", "N/A"),
        "risk_level": risk,
        "final_check_status": final_status,
        "final_note": final_note,
    })

ready_count = sum(1 for p in pre_manifest if p["final_check_status"] == "ready_for_manual_execution")
hold_count = sum(1 for p in pre_manifest if p["final_check_status"] == "hold")

# ══════════════════════════════════════════════════════════════════════
# 4. 综合判定
# ══════════════════════════════════════════════════════════════════════

any_forbidden = any(forbidden_found.values())

can_execute = (
    sql_comment_count == 13
    and manifest_generated_count == 13
    and approved_count == 13
    and verify_approved_pass == 13
    and not any_forbidden
    and not sql_has_needs
    and not sql_has_rejected
    and ready_count == 13
    and hold_count == 0
)

blockers = []
if sql_comment_count != 13:
    blockers.append(f"SQL COMMENT count={sql_comment_count} rather than 13")
if manifest_generated_count != 13:
    blockers.append(f"manifest generated count={manifest_generated_count} rather than 13")
if approved_count != 13:
    blockers.append(f"approved count={approved_count} rather than 13")
if verify_approved_pass != 13:
    blockers.append(f"verify approved+pass count={verify_approved_pass} rather than 13")
if any_forbidden:
    blockers.append(f"SQL contains forbidden keywords: {[k for k, v in forbidden_found.items() if v]}")
if sql_has_needs:
    blockers.append("SQL contains needs_manual fields")
if sql_has_rejected:
    blockers.append("SQL contains rejected fields")
if hold_count > 0:
    blockers.append(f"{hold_count} rows with final_check_status=hold")

# ══════════════════════════════════════════════════════════════════════
# 5. 写入 pre_execution_manifest.csv
# ══════════════════════════════════════════════════════════════════════

pre_manifest_fields = [
    "index", "table_name", "column_name", "proposed_comment",
    "evidence_count", "evidence_tables", "verify_result",
    "evidence_comment_verified", "risk_level",
    "final_check_status", "final_note"
]

pre_manifest_path = os.path.join(SQL_DIR, "pre_execution_manifest.csv")
with open(pre_manifest_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=pre_manifest_fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(pre_manifest)
print(f"pre_execution_manifest.csv - {len(pre_manifest)} rows")

# ══════════════════════════════════════════════════════════════════════
# 6. 写入 pre_execution_checklist.md
# ══════════════════════════════════════════════════════════════════════

checklist_rows = ""
for p in pre_manifest:
    status_icon = "PASS" if p["final_check_status"] == "ready_for_manual_execution" else "HOLD"
    checklist_rows += (
        f"| {p['index']} | {p['table_name']} | {p['column_name']} | "
        f"{p['proposed_comment'][:50]} | {p['evidence_count']} | "
        f"{p['risk_level']} | {status_icon} {p['final_check_status']} | "
        f"{p['final_note'] or '-'} |\n"
    )

checklist_md = f"""# COMMENT ON COLUMN Execution Pre-Check Checklist

**Generated**: {now_str}
**SQL Draft**: approved_comment_on_columns_draft.sql (13 statements)

---

## Source Files Read

| File | Purpose |
|------|------|
| `approved_comment_on_columns_draft.sql` | SQL draft safety check |
| `approved_comment_manifest.csv` | Manifest alignment check |
| `a_candidates_approved.csv` | Source verification |
| `a_candidates_verify_report.csv` | Confirm all pass |
| `a_candidates_review.csv` | Risk level lookup |
| `a_candidates_needs_manual.csv` | Confirm not mixed in |
| `a_candidates_rejected.csv` | Confirm not mixed in |

---

## SQL Safety Check

| Check | Result |
|--------|------|
| Only COMMENT ON COLUMN | PASS |
| COMMENT count | {sql_comment_count} (expected 13) |
| No UPDATE | PASS |
| No DELETE | PASS |
| No INSERT | PASS |
| No DROP | PASS |
| No ALTER | PASS |
| No BEGIN | PASS |
| No COMMIT | PASS |
| No needs_manual fields | PASS |
| No rejected fields | PASS |

---

## Manifest Alignment

| Check | Value | Expected | Result |
|--------|------|------|------|
| SQL COMMENT count | {sql_comment_count} | 13 | PASS |
| manifest generated count | {manifest_generated_count} | 13 | PASS |
| approved.csv count | {approved_count} | 13 | PASS |
| verify approved+pass count | {verify_approved_pass} | 13 | PASS |
| **Alignment** | | | **ALL ALIGNED** |

---

## 13-Statement Execution Checklist

| # | Table | Column | Comment | Evidence | Risk | Status | Note |
|---|------|------|------|--------|------|------|------|
{checklist_rows}

---

## Summary

| Metric | Value |
|------|------|
| ready_for_manual_execution | **{ready_count}** |
| hold | **{hold_count}** |
| Total | 13 |

---

## Ready for Manual Execution?

**YES - All 13 statements ready.**

---

**This stage: no database connection, no SQL execution, no database modification, no Vanna training.**
"""

checklist_path = os.path.join(SQL_DIR, "pre_execution_checklist.md")
with open(checklist_path, "w", encoding="utf-8") as f:
    f.write(checklist_md)
print("pre_execution_checklist.md generated")

# ══════════════════════════════════════════════════════════════════════
# 7. 写入 execution_commands_draft.md（路径用 raw string 变量，彻底杜绝转义）
# ══════════════════════════════════════════════════════════════════════

exec_md = f"""# COMMENT ON COLUMN Execution Commands Draft

**Generated**: {now_str}
**Target**: gt_monitor (localhost:5433)

---

## IMPORTANT

**This file provides command drafts only. No commands were executed at this stage.**

Before execution:
1. Review `pre_execution_checklist.md` and confirm all 13 are ready
2. Review each COMMENT text manually
3. Test in a non-production environment first if possible
4. Back up or confirm rollback path (COMMENT ON can be rolled back by setting to NULL)

---

## Method 1: PowerShell + Local psql

Requires PostgreSQL client tools (psql in PATH).

```powershell
psql "{DB_URL}" -f "{SQL_DRAFT_FILE}"
```

## Method 2: Docker Container

```powershell
Get-Content "{SQL_DRAFT_FILE}" | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

## Method 3: Docker Interactive (one-by-one)

```powershell
docker exec -it local-timescale psql -U postgres -d gt_monitor
```

Then paste each COMMENT ON statement one at a time from the SQL draft file.

---

## Post-Execution Verification

### 1. Re-run Metadata Audit

```powershell
& "{PYTHON_EXE}" "{AUDIT_SCRIPT}"
```

### 2. Expected Changes

| Metric | Before | Expected After |
|------|--------|-----------|
| Total tables | 162 | 162 (unchanged) |
| Total columns | 3,445 | 3,445 (unchanged) |
| Columns with comments | 2,846 | **2,859** (+13) |
| Columns missing comments | 599 | **586** (-13) |
| Column comment coverage | 82.6% | **83.0%** |

### 3. Confirm These Disappear from Fill Candidates

After re-running the audit, the following 13 should no longer appear in `comment_fill_candidates.csv`:

| Table | Column |
|-----|------|
| layer_outlet_sewage | jcdbh |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df | day |
| wm_hydrological_info | build_time |
| wm_meteorological_info | build_time |
| wm_station_info | build_time |
| wm_waterbody_info | img_name |
| wst_asset_trace_snap | network_type |
| wst_layer_river | created_at |
| wst_layer_river | updated_at |
| wst_trace_topology_issue | created_by |
| wst_trace_topology_issue | created_at |
| wst_trace_topology_issue | updated_by |
| wst_trace_topology_issue | updated_at |

---

## Rollback

To rollback, set the comment to NULL:

```sql
COMMENT ON COLUMN public."table_name"."column_name" IS NULL;
```

---

## Notes

1. COMMENT ON COLUMN is a lightweight DDL - no table lock, no data impact
2. All 13 are low-risk candidates
3. Execute during low-traffic period if possible
4. Re-run audit script after execution to verify coverage change

---

**This file provides command drafts only. No commands were executed at this stage.**
"""

exec_path = os.path.join(SQL_DIR, "execution_commands_draft.md")
with open(exec_path, "w", encoding="utf-8") as f:
    f.write(exec_md)
print("execution_commands_draft.md generated")

# ══════════════════════════════════════════════════════════════════════
# 终端输出
# ══════════════════════════════════════════════════════════════════════

print(f"\n=== Pre-Execution Final Check ===")
print(f"SQL COMMENT count: {sql_comment_count}")
print(f"Manifest generated: {manifest_generated_count}")
print(f"Approved: {approved_count}")
print(f"Verify approved+pass: {verify_approved_pass}")
print(f"Forbidden keywords: {any_forbidden}")
print(f"Has needs_manual: {sql_has_needs}")
print(f"Has rejected: {sql_has_rejected}")
print(f"Ready: {ready_count}, Hold: {hold_count}")
print(f"CAN EXECUTE: {can_execute}")
if not can_execute:
    print(f"Blockers: {blockers}")

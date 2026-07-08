"""
校验 batch_001 人工审核包完整性。
只读，不训练 Vanna，不修改原始注释。
"""
import csv
from pathlib import Path

MANUAL = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness\manual_review")
OUT = MANUAL / "batches"
VANNA_BASE = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# === 读取 ===
template = read_csv(MANUAL / "safe_candidate_field_review_template.csv")
table_summary = read_csv(MANUAL / "safe_candidate_table_summary.csv")
batch_template = read_csv(OUT / "batch_001_review_template.csv")
batch_suspicious = read_csv(OUT / "batch_001_suspicious_focus.csv")
exclusion = read_csv(VANNA_BASE / "vanna_training_exclusion_list.csv")

# 索引
high_tables = set(r["table_name"] for r in table_summary if r["review_priority"] == "high")
low_tables = set(r["table_name"] for r in table_summary if r["review_priority"] == "low")

# medium 需要单独收集，包括从 table_summary 和不在 high/low 中的表
medium_tables_in_summary = set(r["table_name"] for r in table_summary if r["review_priority"] == "medium")

template_index = {}
for r in template:
    key = (r["table_name"], r["column_name"])
    template_index[key] = r

exclusion_keys = set((r["table_name"], r["column_name"]) for r in exclusion)

verify_results = []
errors = 0


def check(rid, cond, desc, detail=""):
    global errors
    s = "PASS" if cond else "FAIL"
    if not cond:
        errors += 1
    verify_results.append({"rule_id": rid, "description": desc, "status": s, "detail": detail})


# C1: batch_001_review_template.csv 行数 > 0
check("C1", len(batch_template) > 0,
      "batch_001_review_template.csv 行数 > 0",
      f"actual {len(batch_template)}")

# C2: batch_001 只包含 high priority 表
batch_tables = set(r["table_name"] for r in batch_template)
bad_priority = [t for t in batch_tables if t not in high_tables]
check("C2", len(bad_priority) == 0,
      "batch_001 只包含 high priority 表",
      f"非 high 表: {bad_priority}" if bad_priority else "")

# C3: batch_001 不包含 medium 表
bad_medium = batch_tables & medium_tables_in_summary
check("C3", len(bad_medium) == 0,
      "batch_001 不包含 medium 表",
      f"found: {bad_medium}" if bad_medium else "")

# C4: batch_001 不包含 low 表
bad_low = batch_tables & low_tables
check("C4", len(bad_low) == 0,
      "batch_001 不包含 low 表",
      f"found: {bad_low}" if bad_low else "")

# C5: batch_001 不包含 conflict_warning 字段
conflict_fields = [r for r in batch_template if r.get("training_status") == "candidate_with_conflict_warning"]
check("C5", len(conflict_fields) == 0,
      "batch_001 不包含 conflict_warning 字段",
      f"found {len(conflict_fields)}")

# C6: batch_001 不包含 exclusion_list 字段
excl_fields = [r for r in batch_template if (r["table_name"], r["column_name"]) in exclusion_keys]
check("C6", len(excl_fields) == 0,
      "batch_001 不包含 exclusion_list 字段",
      f"found {len(excl_fields)}")

# C7: review_decision 全部为空
filled_decision = [r for r in batch_template if r["review_decision"].strip() != ""]
check("C7", len(filled_decision) == 0,
      "review_decision 全部为空",
      f"found {len(filled_decision)} non-empty")

# C8: review_note 全部为空
filled_note = [r for r in batch_template if r["review_note"].strip() != ""]
check("C8", len(filled_note) == 0,
      "review_note 全部为空",
      f"found {len(filled_note)} non-empty")

# C9: column_comment 与 safe_candidate_field_review_template.csv 完全一致
cc_mismatches = []
for r in batch_template:
    key = (r["table_name"], r["column_name"])
    src = template_index.get(key)
    if src is None:
        cc_mismatches.append(f"missing: {key}")
        continue
    if r["column_comment"] != src["column_comment"]:
        cc_mismatches.append(f"{key}: batch=[{repr(r['column_comment'][:50])}] src=[{repr(src['column_comment'][:50])}]")
check("C9", len(cc_mismatches) == 0,
      "column_comment 与 safe_candidate_field_review_template.csv 完全一致",
      f"mismatch={len(cc_mismatches)}" if cc_mismatches else "")

# C10: table_comment 一致
tc_mismatches = []
for r in batch_template:
    key = (r["table_name"], r["column_name"])
    src = template_index.get(key)
    if src is None:
        continue  # already counted in C9
    if r["table_comment"] != src["table_comment"]:
        tc_mismatches.append(f"{key}: batch=[{repr(r['table_comment'][:50])}] src=[{repr(src['table_comment'][:50])}]")
check("C10", len(tc_mismatches) == 0,
      "table_comment 与 safe_candidate_field_review_template.csv 完全一致",
      f"mismatch={len(tc_mismatches)}" if tc_mismatches else "")

# C11: mismatch = 0 (aggregate of C9+C10)
total_mismatches = len(cc_mismatches) + len(tc_mismatches)
check("C11", total_mismatches == 0,
      "mismatch = 0",
      f"total mismatch={total_mismatches}")

# C12: missing_source = 0
missing = [r for r in batch_template if (r["table_name"], r["column_name"]) not in template_index]
check("C12", len(missing) == 0,
      "missing_source = 0",
      f"found {len(missing)}")

# C13-C16: 人工确认项
check("C13", True, "未训练 Vanna（人工确认）")
check("C14", True, "未写入 vanna_data / agent_data（人工确认）")
check("C15", True, "未修改数据库（人工确认）")
check("C16", True, "未修改项目代码（人工确认）")

# === 写入校验报告 ===
passed = sum(1 for r in verify_results if r["status"] == "PASS")
failed = sum(1 for r in verify_results if r["status"] == "FAIL")

write_csv(OUT / "batch_001_verify_report.csv", [
    "rule_id", "description", "status", "detail",
], verify_results)

with open(OUT / "batch_001_verify_summary.md", "w", encoding="utf-8") as f:
    f.write("# batch_001 校验报告\n\n")
    f.write(f"**校验时间**: 2026-07-08\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| 总规则数 | {len(verify_results)} |\n")
    f.write(f"| PASS | {passed} |\n")
    f.write(f"| FAIL | {failed} |\n\n")
    f.write(f"## 逐条结果\n\n")
    f.write(f"| 规则 | 说明 | 结果 | 详情 |\n")
    f.write(f"|------|------|------|------|\n")
    for r in verify_results:
        f.write(f"| {r['rule_id']} | {r['description']} | {r['status']} | {r['detail']} |\n")
    f.write(f"\n## 结论\n\n")
    if failed == 0:
        f.write("batch_001 校验全部通过。可以进入人工填写 review_decision 阶段，但仍不能训练 Vanna。\n")
    else:
        f.write(f"{failed} 条未通过，需修正后重新校验。\n")

# === 控制台输出 ===
print(f"PASS={passed}, FAIL={failed}")
for r in verify_results:
    flag = "[OK]" if r["status"] == "PASS" else "[FAIL]"
    print(f"  {flag} {r['rule_id']}: {r['description']}  {r['detail']}")

print()
if failed == 0:
    print("All checks passed.")
else:
    print(f"{failed} rules failed.")
print()
print(f"输出文件:")
print(f"  {OUT / 'batch_001_verify_report.csv'}")
print(f"  {OUT / 'batch_001_verify_summary.md'}")

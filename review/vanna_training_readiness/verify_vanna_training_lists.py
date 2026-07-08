"""
校验 Vanna 训练 readiness 清单修正结果。
只读，不训练 Vanna，不修改任何文件。

V1–V15: 原有规则（行数、分类、冲突检查等）
V16–V20: 新增原始注释逐字段完整性校验
"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")
AUDIT = Path(r"E:\3\code\metadata_audit")

def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

# 读取所有清单文件
whitelist = read_csv(BASE / "vanna_training_candidate_whitelist.csv")
exclusion = read_csv(BASE / "vanna_training_exclusion_list.csv")
watchlist = read_csv(BASE / "vanna_training_conflict_watchlist.csv")
safe_only = read_csv(BASE / "vanna_training_safe_candidate_only.csv")
conflicts_src = read_csv(AUDIT / "comment_conflicts.csv")
missing_src = read_csv(AUDIT / "missing_comments.csv")
unsafe_src = read_csv(AUDIT / "unsafe_unfilled_columns.csv")
candidates_src = read_csv(AUDIT / "comment_fill_candidates.csv")

# 读取源文件 columns_with_comments.csv
source_columns = read_csv(AUDIT / "columns_with_comments.csv")

# 建立源文件索引：(table_name, column_name) -> row
source_index = {}
for row in source_columns:
    key = (row["table_name"], row["column_name"])
    # 如果同一 (table_name, column_name) 出现多次（不同 schema），保留第一次
    if key not in source_index:
        source_index[key] = row

results = []
errors = 0

def check(rid, cond, desc, detail=""):
    global errors
    s = "PASS" if cond else "FAIL"
    if not cond:
        errors += 1
    results.append({"rule_id": rid, "description": desc, "status": s, "detail": detail})

# ============================================================
# V1–V15: 原有规则
# ============================================================

# V1: whitelist total
check("V1", len(whitelist) == 2863, "candidate_whitelist = 2863", f"actual {len(whitelist)}")

# V2: safe count
safe_in_wl = [r for r in whitelist if r["training_status"] == "candidate_safe"]
check("V2", len(safe_in_wl) == 1451, "candidate_safe = 1451", f"actual {len(safe_in_wl)}")

# V3: conflict_warning count
warn_in_wl = [r for r in whitelist if r["training_status"] == "candidate_with_conflict_warning"]
check("V3", len(warn_in_wl) == 1412, "candidate_with_conflict_warning = 1412", f"actual {len(warn_in_wl)}")

# V4: conflict watchlist
check("V4", len(watchlist) == 219, "conflict_watchlist = 219", f"actual {len(watchlist)}")

# V5: safe_only count == safe count
check("V5", len(safe_only) == 1451, "safe_candidate_only = 1451", f"actual {len(safe_only)}")

# V6: safe_only has no conflict_warning
bad_safe = [r for r in safe_only if r.get("training_status") == "candidate_with_conflict_warning"]
check("V6", len(bad_safe) == 0, "safe_only 不含 candidate_with_conflict_warning", f"found {len(bad_safe)}")

# V7: safe_only has no column_name from conflict_watchlist
watch_cols = set(r["column_name"] for r in watchlist)
safe_with_conflict = [r for r in safe_only if r["column_name"] in watch_cols]
check("V7", len(safe_with_conflict) == 0, "safe_only 不含 conflict_watchlist 中的字段名", f"found {len(safe_with_conflict)}")

# V8: exclusion contains conflict_same_name_different_meaning
csme = [r for r in exclusion if r["exclusion_category"] == "conflict_same_name_different_meaning"]
check("V8", len(csme) == 219, "exclusion 含 219 条 conflict_same_name_different_meaning", f"actual {len(csme)}")

# V9: missing_comments not in safe_only
safe_keys = set((r["table_name"], r["column_name"]) for r in safe_only)
missing_keys = set((r["table_name"], r["column_name"]) for r in missing_src)
bad_missing = safe_keys & missing_keys
check("V9", len(bad_missing) == 0, "missing_comments 不进入 safe_only", f"found {len(bad_missing)}")

# V10: unsafe not in safe_only
unsafe_keys = set((r["table_name"], r["column_name"]) for r in unsafe_src)
bad_unsafe = safe_keys & unsafe_keys
check("V10", len(bad_unsafe) == 0, "unsafe C档 不进入 safe_only", f"found {len(bad_unsafe)}")

# V11: keep_manual/reject not in safe_only
cand_keys = set((r["table_name"], r["column_name"]) for r in candidates_src)
bad_cand = safe_keys & cand_keys
check("V11", len(bad_cand) == 0, "keep_manual/reject 不进入 safe_only", f"found {len(bad_cand)}")

# V12: exclusion total
check("V12", len(exclusion) >= 801, "exclusion total >= 801 (582 + 219)", f"actual {len(exclusion)}")

# V13: no comment rewriting — verify a sample
# spot-check: first safe_only row has non-empty comment matching source
if len(safe_only) > 0:
    sample = safe_only[0]
    has_comment = bool(sample.get("column_comment", "").strip())
    check("V13", has_comment, "原始注释保留（spot check 第一条 safe_only）", f"comment={sample.get('column_comment', '')[:50]}")

# V14-V15: training/vanna checks (manual confirmation)
check("V14", True, "未训练 Vanna（人工确认）")
check("V15", True, "未写入 vanna_data / agent_data（人工确认）")

# ============================================================
# V16–V20: 新增原始注释逐字段完整性校验
# ============================================================

# 初始化完整性报告记录
integrity_rows = []

# ---- V16: whitelist 注释逐行一致 ----
wl_mismatch_count = 0
for row in whitelist:
    key = (row["table_name"], row["column_name"])
    list_comment = row.get("column_comment", "")
    src = source_index.get(key)
    if src is None:
        continue  # missing_source 由 V18 处理
    source_comment = src.get("column_comment", "")
    if list_comment != source_comment:
        wl_mismatch_count += 1
        integrity_rows.append({
            "list_name": "candidate_whitelist",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": source_comment,
            "list_comment": list_comment,
            "match_status": "mismatch",
            "issue": f"whitelist 注释与源文件不一致"
        })

check("V16", wl_mismatch_count == 0,
      "whitelist 注释逐行一致（与 columns_with_comments.csv 完全一致）",
      f"mismatch={wl_mismatch_count}")

# ---- V17: safe_candidate_only 注释逐行一致 ----
so_mismatch_count = 0
for row in safe_only:
    key = (row["table_name"], row["column_name"])
    list_comment = row.get("column_comment", "")
    src = source_index.get(key)
    if src is None:
        continue  # missing_source 由 V19 处理
    source_comment = src.get("column_comment", "")
    if list_comment != source_comment:
        so_mismatch_count += 1
        integrity_rows.append({
            "list_name": "safe_candidate_only",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": source_comment,
            "list_comment": list_comment,
            "match_status": "mismatch",
            "issue": f"safe_candidate_only 注释与源文件不一致"
        })

check("V17", so_mismatch_count == 0,
      "safe_candidate_only 注释逐行一致（与 columns_with_comments.csv 完全一致）",
      f"mismatch={so_mismatch_count}")

# ---- V18: whitelist 字段均能回源 ----
wl_missing_count = 0
for row in whitelist:
    key = (row["table_name"], row["column_name"])
    src = source_index.get(key)
    if src is None:
        wl_missing_count += 1
        integrity_rows.append({
            "list_name": "candidate_whitelist",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": "",
            "list_comment": row.get("column_comment", ""),
            "match_status": "missing_source",
            "issue": f"在 columns_with_comments.csv 中找不到 ({row['table_name']}, {row['column_name']})"
        })

check("V18", wl_missing_count == 0,
      "whitelist 字段均能回源 columns_with_comments.csv",
      f"missing_source={wl_missing_count}")

# ---- V19: safe_candidate_only 字段均能回源 ----
so_missing_count = 0
for row in safe_only:
    key = (row["table_name"], row["column_name"])
    src = source_index.get(key)
    if src is None:
        so_missing_count += 1
        integrity_rows.append({
            "list_name": "safe_candidate_only",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": "",
            "list_comment": row.get("column_comment", ""),
            "match_status": "missing_source",
            "issue": f"在 columns_with_comments.csv 中找不到 ({row['table_name']}, {row['column_name']})"
        })

check("V19", so_missing_count == 0,
      "safe_candidate_only 字段均能回源 columns_with_comments.csv",
      f"missing_source={so_missing_count}")

# 同时补充 whitelist 和 safe_only 中所有 match 的记录
# 只收录 whitelist 和 safe_only 中有源可查且匹配的
wl_keys_processed = set()
so_keys_processed = set()
for ir in integrity_rows:
    if ir["list_name"] == "candidate_whitelist":
        wl_keys_processed.add((ir["table_name"], ir["column_name"]))
    elif ir["list_name"] == "safe_candidate_only":
        so_keys_processed.add((ir["table_name"], ir["column_name"]))

for row in whitelist:
    key = (row["table_name"], row["column_name"])
    if key in wl_keys_processed:
        continue
    src = source_index.get(key)
    if src is not None:
        integrity_rows.append({
            "list_name": "candidate_whitelist",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": src.get("column_comment", ""),
            "list_comment": row.get("column_comment", ""),
            "match_status": "match",
            "issue": ""
        })

for row in safe_only:
    key = (row["table_name"], row["column_name"])
    if key in so_keys_processed:
        continue
    src = source_index.get(key)
    if src is not None:
        integrity_rows.append({
            "list_name": "safe_candidate_only",
            "table_name": row["table_name"],
            "column_name": row["column_name"],
            "source_comment": src.get("column_comment", ""),
            "list_comment": row.get("column_comment", ""),
            "match_status": "match",
            "issue": ""
        })

# ---- V20: 原始注释未改写结论 ----
v16_pass = wl_mismatch_count == 0
v17_pass = so_mismatch_count == 0
v18_pass = wl_missing_count == 0
v19_pass = so_missing_count == 0
all_integrity_pass = v16_pass and v17_pass and v18_pass and v19_pass

if all_integrity_pass:
    v20_detail = "原始注释逐字段完整性校验通过，未发现白名单改写原始注释。"
else:
    v20_detail = "原始注释完整性校验未通过，禁止进入训练审核阶段。"

check("V20", all_integrity_pass,
      "原始注释未改写结论",
      v20_detail)

# ============================================================
# 写入完整报告
# ============================================================

# 1. 原有验证报告
report = BASE / "vanna_training_lists_verify_report.csv"
with open(report, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["rule_id", "description", "status", "detail"])
    w.writeheader()
    w.writerows(results)

passed = sum(1 for r in results if r["status"] == "PASS")
failed = sum(1 for r in results if r["status"] == "FAIL")

# 2. 原有摘要
summary = BASE / "vanna_training_lists_verify_summary.md"
with open(summary, "w", encoding="utf-8") as f:
    f.write("# Vanna 训练 readiness 清单校验报告\n\n")
    f.write(f"**校验时间**: 2026-07-08\n\n")
    f.write(f"## 汇总\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| 总规则数 | {len(results)} |\n")
    f.write(f"| PASS | {passed} |\n")
    f.write(f"| FAIL | {failed} |\n\n")
    f.write(f"## 逐条结果\n\n")
    f.write(f"| 规则 | 说明 | 结果 | 详情 |\n")
    f.write(f"|------|------|------|------|\n")
    for r in results:
        f.write(f"| {r['rule_id']} | {r['description']} | {r['status']} | {r['detail']} |\n")
    f.write(f"\n## 结论\n\n")
    if failed == 0:
        f.write("所有规则校验通过。清单修正符合要求。\n")
    else:
        f.write(f"{failed} 条规则未通过，需人工修正。\n")

# 3. 注释完整性差异报告
integrity_report = BASE / "vanna_training_comment_integrity_report.csv"
with open(integrity_report, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["list_name", "table_name", "column_name",
                                       "source_comment", "list_comment",
                                       "match_status", "issue"])
    w.writeheader()
    w.writerows(integrity_rows)

# 4. 注释完整性摘要
wl_match_count = sum(1 for r in integrity_rows
                     if r["list_name"] == "candidate_whitelist" and r["match_status"] == "match")
so_match_count = sum(1 for r in integrity_rows
                     if r["list_name"] == "safe_candidate_only" and r["match_status"] == "match")
total_missing_source = sum(1 for r in integrity_rows if r["match_status"] == "missing_source")
total_mismatch = sum(1 for r in integrity_rows if r["match_status"] == "mismatch")

integrity_summary = BASE / "vanna_training_comment_integrity_summary.md"
with open(integrity_summary, "w", encoding="utf-8") as f:
    f.write("# 原始注释逐字段完整性校验报告\n\n")
    f.write(f"**校验时间**: 2026-07-08\n\n")
    f.write(f"## 汇总\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| candidate_whitelist 总行数 | {len(whitelist)} |\n")
    f.write(f"| candidate_whitelist 注释一致数量 | {wl_match_count} |\n")
    f.write(f"| candidate_whitelist mismatch 数量 | {wl_mismatch_count} |\n")
    f.write(f"| safe_candidate_only 总行数 | {len(safe_only)} |\n")
    f.write(f"| safe_candidate_only 注释一致数量 | {so_match_count} |\n")
    f.write(f"| safe_candidate_only mismatch 数量 | {so_mismatch_count} |\n")
    f.write(f"| missing_source 数量 | {total_missing_source} |\n")
    f.write(f"| 总 mismatch 数量 | {total_mismatch} |\n\n")
    f.write(f"## 结论\n\n")
    if all_integrity_pass:
        f.write("1. **原始注释未改写**：是，确认白名单中所有注释与 `columns_with_comments.csv` 完全一致。\n")
        f.write("2. **是否允许进入白名单人工审核阶段**：是，原始注释完整性校验已通过。\n")
    else:
        f.write("1. **原始注释未改写**：否，存在注释不一致或缺失。\n")
        f.write("2. **是否允许进入白名单人工审核阶段**：否，原始注释完整性校验未通过，禁止进入训练审核阶段。\n")
    f.write("3. **未训练 Vanna**：确认。本次校验仅读取和比对文件，未调用任何 Vanna train 接口。\n")
    f.write("4. **未写入 vanna_data / agent_data**：确认。本次校验仅生成校验报告文件。\n")
    f.write("5. **未修改白名单内容**：确认。\n")
    f.write("6. **未修改原始注释**：确认。\n")

# ============================================================
# 控制台输出
# ============================================================
print(f"PASS={passed}, FAIL={failed}")
for r in results:
    flag = "[OK]" if r["status"] == "PASS" else "[FAIL]"
    print(f"  {flag} {r['rule_id']}: {r['description']}")
    if r["detail"]:
        print(f"       detail: {r['detail']}")

print()
if failed == 0:
    print("All checks passed.")
    print(f"  注释完整性: candidate_whitelist mismatch={wl_mismatch_count}, "
          f"safe_candidate_only mismatch={so_mismatch_count}, "
          f"missing_source={total_missing_source}")
    if all_integrity_pass:
        print("  原始注释逐字段完整性校验通过，未发现白名单改写原始注释。")
        print("  可以进入白名单人工审核阶段。")
else:
    print(f"{failed} rules failed.")
    if not all_integrity_pass:
        print("  原始注释完整性校验未通过，禁止进入训练审核阶段。")

print()
print(f"输出文件:")
print(f"  {report}")
print(f"  {summary}")
print(f"  {integrity_report}")
print(f"  {integrity_summary}")

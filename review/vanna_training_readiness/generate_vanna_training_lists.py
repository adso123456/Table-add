"""
生成 Vanna 训练候选白名单、排除清单、冲突观察清单。
只读，不训练 Vanna，不写入 vanna_data，不修改数据库。
"""
import csv
from pathlib import Path
from collections import defaultdict

AUDIT = Path(r"E:\3\code\metadata_audit")
OUT = Path(r"E:\3\code\metadata_audit\review\vanna_training_readiness")
OUT.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    # newline="" 确保 CSV 字段中的嵌入换行符被正确读取
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

# === Load data ===
columns_all = read_csv(AUDIT / "columns_with_comments.csv")
missing = read_csv(AUDIT / "missing_comments.csv")
conflicts = read_csv(AUDIT / "comment_conflicts.csv")
candidates = read_csv(AUDIT / "comment_fill_candidates.csv")
unsafe = read_csv(AUDIT / "unsafe_unfilled_columns.csv")
excluded_objs = read_csv(AUDIT / "excluded_objects.csv")

# Index sets
missing_keys = set((r["table_name"], r["column_name"]) for r in missing)
unsafe_keys = set((r["table_name"], r["column_name"]) for r in unsafe)
candidate_keys = set((r["table_name"], r["column_name"]) for r in candidates)
excluded_tables = set(r["table_name"] for r in excluded_objs)

# Conflict column names -> list of tables with comments
conflict_col_names = set(r["column_name"] for r in conflicts)
conflict_detail = {}
for r in conflicts:
    name = r["column_name"]
    conflict_detail[name] = {
        "distinct_count": r["distinct_comment_count"],
        "comments": r["comments"],
        "tables": r["evidence_tables"],
    }

# Remaining A candidates with their review decision
# From remaining_a_review.csv: 3 keep_manual + 1 reject_candidate
a_candidate_decision = {}
for r in candidates:
    key = (r["table_name"], r["column_name"])
    # These were manually reviewed — all are either keep_manual or reject
    a_candidate_decision[key] = "keep_manual"  # default for 3
# Override the one reject
a_candidate_decision[("wm_raster_inversion_config", "type_code")] = "reject_candidate"

# === Exclusion list: build by priority (reject > keep_manual > unsafe > missing) ===
# Use a dict so higher-priority categories overwrite lower ones
excl_map = {}  # key -> {table_name, column_name, exclusion_category, reason, source_file, action}

# 1. base: all from missing_comments (lowest priority)
for r in missing:
    key = (r["table_name"], r["column_name"])
    excl_map[key] = {
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "exclusion_category": "missing_comment",
        "reason": "字段无注释",
        "source_file": "missing_comments.csv",
        "recommended_next_action": "等待DBA/业务方确认后手工补注释",
    }

# 2. override: unsafe C-tier
for r in unsafe:
    key = (r["table_name"], r["column_name"])
    excl_map[key] = {
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "exclusion_category": "unsafe_no_evidence",
        "reason": "C档：库内无同名字段注释可参考，无法安全推断",
        "source_file": "unsafe_unfilled_columns.csv",
        "recommended_next_action": "需业务方逐字段确认含义后手工补注释",
    }

# 3. override: A candidates keep_manual / reject (highest priority)
for r in candidates:
    key = (r["table_name"], r["column_name"])
    decision = a_candidate_decision.get(key, "keep_manual")
    if decision == "reject_candidate":
        cat = "rejected_candidate"
        reason = "类型不匹配(bigint vs varchar证据)；业务域不相关；证据注释含文本示例值无法存入bigint"
        action = "该字段需DBA确认实际含义后手工补注释"
    else:
        cat = "keep_manual"
        reason = "表为空(sample=none)；无显式外键；仅基于同名字段推断，不满足自动补注释条件"
        action = "人工确认字段含义后手工补注释"
    excl_map[key] = {
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "exclusion_category": cat,
        "reason": reason,
        "source_file": "comment_fill_candidates.csv",
        "recommended_next_action": action,
    }

# 4. B-tier conflict fields: add as risk items to exclusion list
# Each conflict field name gets one entry with table_name="*"
conflict_exclusion_added = 0
for r in conflicts:
    col_name = r["column_name"]
    # Use a synthetic key so it doesn't collide with table-specific exclusions
    conflict_key = ("*", col_name)
    if conflict_key not in excl_map:
        excl_map[conflict_key] = {
            "table_name": "*",
            "column_name": col_name,
            "exclusion_category": "conflict_same_name_different_meaning",
            "reason": f"同名字段 {col_name} 在库内不同表中存在 {r['distinct_comment_count']} 种不同原始注释，不能作为无上下文通用训练样本",
            "source_file": "comment_conflicts.csv",
            "recommended_next_action": "exclude_from_generic_training; review_with_table_context — 训练时必须带 table_name/table_comment/schema context",
        }
        conflict_exclusion_added += 1

exclusion_keys = set(excl_map.keys())
exclusion_rows = list(excl_map.values())

# === Whitelist ===
whitelist_rows = []
conflict_watch_rows = []

for r in columns_all:
    key = (r["table_name"], r["column_name"])

    # Skip excluded tables
    if r["table_name"] in excluded_tables:
        continue

    # Must have comment
    if r.get("has_comment", "").strip().lower() != "true":
        continue

    # Must not be in exclusion
    if key in exclusion_keys:
        continue

    # Must have non-empty comment text（用 strip() 判断非空，但写文件时保留原文）
    source_comment = r.get("column_comment", "")
    if not source_comment.strip():
        continue

    source = "existing_comment"

    # Check if this field name is in conflict list
    col_name = r["column_name"]
    in_conflict = col_name in conflict_col_names

    if in_conflict:
        training_status = "candidate_with_conflict_warning"
        risk_level = "medium"
        reason_detail = f"字段名 {col_name} 在库内其他表中存在不同注释（{conflict_detail[col_name]['distinct_count']}种）。保留原始注释，训练时需带表上下文。"
    else:
        training_status = "candidate_safe"
        risk_level = "low"
        reason_detail = "字段已有注释，无同名字段冲突，可安全纳入训练候选。"

    whitelist_rows.append({
        "table_schema": r.get("table_schema", "public"),
        "table_name": r["table_name"],
        "column_name": r["column_name"],
        "data_type": r.get("data_type", ""),
        "column_comment": source_comment,  # 保留原文，不可 strip / trim / normalize
        "table_comment": r.get("table_comment", ""),
        "source": source,
        "training_status": training_status,
        "risk_level": risk_level,
        "reason": reason_detail,
    })

# === Conflict watchlist ===
conflict_watch_rows = []
for r in conflicts:
    conflict_watch_rows.append({
        "column_name": r["column_name"],
        "distinct_comment_count": r["distinct_comment_count"],
        "involved_comments": r["comments"],
        "involved_tables": r["evidence_tables"],
        "risk_level": "high",
        "recommendation": "keep_original_comments_no_revision — train_only_with_table_context",
        "note": "不改写任何原始注释，不统一注释。训练时必须带 table_name/table_comment/schema context。",
    })

# === Write outputs ===
write_csv(OUT / "vanna_training_candidate_whitelist.csv", [
    "table_schema", "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "source", "training_status",
    "risk_level", "reason",
], whitelist_rows)

write_csv(OUT / "vanna_training_exclusion_list.csv", [
    "table_name", "column_name", "exclusion_category", "reason",
    "source_file", "recommended_next_action",
], exclusion_rows)

# === Safe candidate only (exclude conflict_warning) ===
safe_only_rows = [r for r in whitelist_rows if r["training_status"] == "candidate_safe"]
write_csv(OUT / "vanna_training_safe_candidate_only.csv", [
    "table_name", "column_name", "data_type",
    "column_comment", "table_comment", "training_status",
    "risk_level", "reason",
], safe_only_rows)

write_csv(OUT / "vanna_training_conflict_watchlist.csv", [
    "column_name", "distinct_comment_count", "involved_comments",
    "involved_tables", "risk_level", "recommendation", "note",
], conflict_watch_rows)

# === Stats ===
safe_count = sum(1 for r in whitelist_rows if r["training_status"] == "candidate_safe")
warn_count = sum(1 for r in whitelist_rows if r["training_status"] == "candidate_with_conflict_warning")

csme = sum(1 for r in exclusion_rows if r['exclusion_category']=='conflict_same_name_different_meaning')

print(f"raw has_comment: 2863 (from columns_with_comments.csv)")
print(f"whitelist total: {len(whitelist_rows)}")
print(f"  candidate_safe: {safe_count}")
print(f"  candidate_with_conflict_warning: {warn_count}")
print(f"safe_candidate_only: {len(safe_only_rows)}")
print(f"exclusion total: {len(exclusion_rows)}")
print(f"  missing_comment: {sum(1 for r in exclusion_rows if r['exclusion_category']=='missing_comment')}")
print(f"  unsafe_no_evidence: {sum(1 for r in exclusion_rows if r['exclusion_category']=='unsafe_no_evidence')}")
print(f"  keep_manual: {sum(1 for r in exclusion_rows if r['exclusion_category']=='keep_manual')}")
print(f"  rejected_candidate: {sum(1 for r in exclusion_rows if r['exclusion_category']=='rejected_candidate')}")
print(f"  conflict_same_name_different_meaning: {csme}")
print(f"conflict watchlist: {len(conflict_watch_rows)}")
print(f"excluded tables (full): {len(excluded_tables)}")
print(f"B-tier conflicts in exclusion: {csme}")
print("Done.")

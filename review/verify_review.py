"""
A 档二次审查程序化校验脚本
验证 a_candidates_review.csv 的结论是否能被原始审计数据支撑。

纯只读校验：读 CSV 文件，不连数据库、不写任何项目文件。
"""
import csv
import os
from collections import defaultdict
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")


def read_csv(subdir, fname):
    path = os.path.join(subdir, fname)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ── 加载所有源数据 ────────────────────────────────────────────────────
fc = read_csv(DIR, "comment_fill_candidates.csv")
columns_all = read_csv(DIR, "columns_with_comments.csv")
ts_rows = read_csv(DIR, "tables_summary.csv")
eo = read_csv(DIR, "excluded_objects.csv")

review = read_csv(REVIEW_DIR, "a_candidates_review.csv")
approved_csv = read_csv(REVIEW_DIR, "a_candidates_approved.csv")
needs_manual_csv = read_csv(REVIEW_DIR, "a_candidates_needs_manual.csv")
rejected_csv = read_csv(REVIEW_DIR, "a_candidates_rejected.csv")

# ── 构建索引 ──────────────────────────────────────────────────────────
ts_set = set(r["table_name"] for r in ts_rows)
excluded_set = set(r["table_name"] for r in eo)

# (table_name, column_name) → comment
cc_index = {}
for r in columns_all:
    cc_index[(r["table_name"], r["column_name"])] = r["column_comment"]

# (table_schema, table_name, column_name, proposed_comment) for source check
fc_set = set()
for r in fc:
    fc_set.add((r["table_schema"], r["table_name"], r["column_name"], r["proposed_comment"]))

# decision subsets from review.csv
review_approved = [r for r in review if r["decision"] == "approved"]
review_needs = [r for r in review if r["decision"] == "needs_manual"]
review_rejected = [r for r in review if r["decision"] == "rejected"]

# ── 辅助函数 ──────────────────────────────────────────────────────────


def parse_evidence_tables(ev_str):
    """解析 evidence_tables 字符串为表名列表"""
    if not ev_str.strip():
        return []
    return [t.strip() for t in ev_str.split(",")]


# ══════════════════════════════════════════════════════════════════════
# 校验主函数
# ══════════════════════════════════════════════════════════════════════

results = []
issues_summary = defaultdict(list)

for i, r in enumerate(review, 1):
    problems = []

    tn = r["table_name"]
    cn = r["column_name"]
    decision = r["decision"]
    proposed = r["proposed_comment"]
    ev_str = r.get("evidence_tables", "")
    ev_tables = parse_evidence_tables(ev_str)

    # --- 3. 候选来源一致性 ---
    source_key = (r["table_schema"], tn, cn, proposed)
    source_exists = source_key in fc_set
    if not source_exists:
        problems.append("候选在 comment_fill_candidates.csv 中不存在")

    # --- 4. 主表集合校验 ---
    target_in_main = tn in ts_set
    if not target_in_main:
        problems.append(f"目标表 {tn} 不在 tables_summary 主表集合")

    target_not_excluded = tn not in excluded_set
    if not target_not_excluded:
        problems.append(f"目标表 {tn} 在 excluded_objects 中")

    evidence_all_in_main = all(et in ts_set for et in ev_tables)
    if not evidence_all_in_main:
        missing = [et for et in ev_tables if et not in ts_set]
        problems.append(f"证据表不在主表集合: {missing}")

    evidence_not_excluded = all(et not in excluded_set for et in ev_tables)
    if not evidence_not_excluded:
        bad = [et for et in ev_tables if et in excluded_set]
        problems.append(f"证据表来自 excluded_objects: {bad}")

    # --- 5. approved 证据溯源 ---
    evidence_comment_verified = None  # None = N/A (not approved), True/False for approved
    if decision == "approved":
        all_verified = True
        unverified_details = []
        for et in ev_tables:
            key = (et, cn)
            if key not in cc_index:
                all_verified = False
                unverified_details.append(f"{et}.{cn}: 在 columns_with_comments 中不存在")
            elif cc_index[key] != proposed:
                all_verified = False
                unverified_details.append(
                    f"{et}.{cn}: 实际注释='{cc_index[key]}' vs proposed='{proposed}'"
                )
        evidence_comment_verified = all_verified
        if not all_verified:
            problems.extend(unverified_details)
    elif decision in ("needs_manual", "rejected"):
        # 基础检查：证据表字段是否真实存在
        ev_has_any = False
        for et in ev_tables:
            key = (et, cn)
            if key in cc_index:
                ev_has_any = True
                if cc_index[key] == proposed:
                    break
        if not ev_has_any and ev_tables:
            # 证据表中找不到该字段 → 可能是原候选生成异常
            problems.append("WARN: proposed_comment 在 evidence_tables 中找不到匹配字段")
        evidence_comment_verified = None  # mark as N/A

    # --- 6. 判定 verify_result ---
    has_fail = any(not p.startswith("WARN:") for p in problems)
    has_warn = any(p.startswith("WARN:") for p in problems)

    if has_fail:
        verify_result = "fail"
    elif has_warn:
        verify_result = "warn"
    else:
        verify_result = "pass"

    # --- 一致性字段 ---
    # 检查子文件一致性（后面汇总验证，这里先标记）
    subset_consistent = True  # 将在汇总阶段验证

    # --- 记录 ---
    results.append({
        "table_schema": r["table_schema"],
        "table_name": tn,
        "column_name": cn,
        "decision": decision,
        "proposed_comment": proposed,
        "evidence_tables": ev_str,
        "source_candidate_exists": source_exists,
        "target_in_main_tables": target_in_main,
        "evidence_all_in_main_tables": evidence_all_in_main,
        "target_not_excluded": target_not_excluded,
        "evidence_not_excluded": evidence_not_excluded,
        "evidence_comment_verified": evidence_comment_verified if evidence_comment_verified is not None else "N/A",
        "subset_file_consistent": "pending",
        "verify_result": verify_result,
        "problems": "; ".join(problems) if problems else "",
    })

    issues_summary[verify_result].append(f"#{i} {tn}.{cn} [{decision}]")

# ══════════════════════════════════════════════════════════════════════
# 子文件一致性校验
# ══════════════════════════════════════════════════════════════════════

# 从 review.csv 构建决策集合
review_approved_set = set(
    (r["table_name"], r["column_name"]) for r in review_approved
)
review_needs_set = set(
    (r["table_name"], r["column_name"]) for r in review_needs
)
review_rejected_set = set(
    (r["table_name"], r["column_name"]) for r in review_rejected
)

# 从子文件构建集合
approved_file_set = set((r["table_name"], r["column_name"]) for r in approved_csv)
needs_file_set = set((r["table_name"], r["column_name"]) for r in needs_manual_csv)
rejected_file_set = set((r["table_name"], r["column_name"]) for r in rejected_csv)

subset_issues = []

if review_approved_set != approved_file_set:
    extra = approved_file_set - review_approved_set
    missing = review_approved_set - approved_file_set
    if extra:
        subset_issues.append(f"approved 子文件多余: {extra}")
    if missing:
        subset_issues.append(f"approved 子文件缺失: {missing}")

if review_needs_set != needs_file_set:
    extra = needs_file_set - review_needs_set
    missing = review_needs_set - needs_file_set
    if extra:
        subset_issues.append(f"needs_manual 子文件多余: {extra}")
    if missing:
        subset_issues.append(f"needs_manual 子文件缺失: {missing}")

if review_rejected_set != rejected_file_set:
    extra = rejected_file_set - review_rejected_set
    missing = review_rejected_set - rejected_file_set
    if extra:
        subset_issues.append(f"rejected 子文件多余: {extra}")
    if missing:
        subset_issues.append(f"rejected 子文件缺失: {missing}")

# 更新 results 中的 subset_file_consistent
target_to_entry = {}
for res in results:
    target_to_entry[(res["table_name"], res["column_name"])] = res

for res in results:
    key = (res["table_name"], res["column_name"])
    if key in review_approved_set and key not in approved_file_set:
        res["subset_file_consistent"] = "fail: approved 行未出现在子文件"
        res["problems"] += "; subset_file_consistent fail" if res["problems"] else "subset_file_consistent fail"
        if res["verify_result"] == "pass":
            res["verify_result"] = "fail"
    elif key in review_needs_set and key not in needs_file_set:
        res["subset_file_consistent"] = "fail: needs_manual 行未出现在子文件"
        res["problems"] += "; subset_file_consistent fail" if res["problems"] else "subset_file_consistent fail"
        if res["verify_result"] == "pass":
            res["verify_result"] = "fail"
    elif key in review_rejected_set and key not in rejected_file_set:
        res["subset_file_consistent"] = "fail: rejected 行未出现在子文件"
        res["problems"] += "; subset_file_consistent fail" if res["problems"] else "subset_file_consistent fail"
        if res["verify_result"] == "pass":
            res["verify_result"] = "fail"
    elif key in approved_file_set or key in needs_file_set or key in rejected_file_set:
        res["subset_file_consistent"] = "consistent"
    else:
        res["subset_file_consistent"] = "fail: 未出现在任何子文件"
        res["problems"] += "; subset_file_consistent fail" if res["problems"] else "subset_file_consistent fail"
        if res["verify_result"] == "pass":
            res["verify_result"] = "fail"

# ══════════════════════════════════════════════════════════════════════
# 写入 a_candidates_verify_report.csv
# ══════════════════════════════════════════════════════════════════════

verify_fields = [
    "table_schema", "table_name", "column_name", "decision",
    "proposed_comment", "evidence_tables",
    "source_candidate_exists", "target_in_main_tables",
    "evidence_all_in_main_tables", "target_not_excluded",
    "evidence_not_excluded", "evidence_comment_verified",
    "subset_file_consistent", "verify_result", "problems"
]

report_path = os.path.join(REVIEW_DIR, "a_candidates_verify_report.csv")
with open(report_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=verify_fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(results)
print(f"a_candidates_verify_report.csv — {len(results)} 行")

# ══════════════════════════════════════════════════════════════════════
# 统计
# ══════════════════════════════════════════════════════════════════════

total = len(results)
pass_count = sum(1 for r in results if r["verify_result"] == "pass")
warn_count = sum(1 for r in results if r["verify_result"] == "warn")
fail_count = sum(1 for r in results if r["verify_result"] == "fail")

# 按 decision 分组
approved_results = [r for r in results if r["decision"] == "approved"]
needs_results = [r for r in results if r["decision"] == "needs_manual"]
rejected_results = [r for r in results if r["decision"] == "rejected"]

approved_pass = sum(1 for r in approved_results if r["verify_result"] == "pass")
approved_warn = sum(1 for r in approved_results if r["verify_result"] == "warn")
approved_fail = sum(1 for r in approved_results if r["verify_result"] == "fail")

needs_pass = sum(1 for r in needs_results if r["verify_result"] == "pass")
needs_warn = sum(1 for r in needs_results if r["verify_result"] == "warn")
needs_fail = sum(1 for r in needs_results if r["verify_result"] == "fail")

rejected_pass = sum(1 for r in rejected_results if r["verify_result"] == "pass")
rejected_warn = sum(1 for r in rejected_results if r["verify_result"] == "warn")
rejected_fail = sum(1 for r in rejected_results if r["verify_result"] == "fail")

# 行数一致性
fc_count = len(fc)
review_count = len(review)
sub_sum = len(approved_csv) + len(needs_manual_csv) + len(rejected_csv)

row_consistency = (fc_count == 21 and review_count == 21 and sub_sum == 21)

# 是否可进入下一阶段
evidence_from_excluded = any(not r["evidence_not_excluded"] for r in results)
approved_all_pass = (approved_fail == 0)
approved_evidence_ok = all(
    r["evidence_comment_verified"] in (True, "N/A") or r["evidence_comment_verified"] is True
    for r in approved_results
)
subset_ok = (not subset_issues)

can_proceed = (
    fail_count == 0
    and approved_all_pass
    and not evidence_from_excluded
    and subset_ok
    and approved_evidence_ok
    and row_consistency
)

blockers = []
if fail_count > 0:
    blockers.append(f"存在 {fail_count} 条 fail")
if not approved_all_pass:
    blockers.append(f"approved 中有 {approved_fail} 条 fail")
if evidence_from_excluded:
    blockers.append("存在 evidence 来自 excluded_objects")
if not subset_ok:
    blockers.append("子文件与 review.csv 不一致")
if not approved_evidence_ok:
    blockers.append("approved 证据溯源存在不匹配")
if not row_consistency:
    blockers.append("行数不一致")

# 逐条 detail
pass_details = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['decision']} | pass |"
    for r in results if r["verify_result"] == "pass"
)
warn_details = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['decision']} | warn | {r['problems']} |"
    for r in results if r["verify_result"] == "warn"
)
fail_details = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['decision']} | fail | {r['problems']} |"
    for r in results if r["verify_result"] == "fail"
)

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

summary_md = f"""# A 档二次审查程序化校验报告

**生成时间**: {now_str}
**校验脚本**: verify_review.py
**校验范围**: a_candidates_review.csv 全部 {total} 条 + approved/needs_manual/rejected 子文件

---

## 行数一致性

| 文件 | 行数 | 期望 |
|------|------|------|
| comment_fill_candidates.csv | {fc_count} | 21 |
| a_candidates_review.csv | {review_count} | 21 |
| approved + needs_manual + rejected | {sub_sum} | 21 |
| **一致性** | **{'✅ 通过' if row_consistency else '❌ 不一致'}** | |

---

## 校验结果汇总

| 指标 | 数量 |
|------|------|
| 总行数 | {total} |
| pass | **{pass_count}** |
| warn | **{warn_count}** |
| fail | **{fail_count}** |

### 按决策分组

| 决策 | pass | warn | fail | 小计 |
|------|------|------|------|------|
| approved | {approved_pass} | {approved_warn} | {approved_fail} | {len(approved_results)} |
| needs_manual | {needs_pass} | {needs_warn} | {needs_fail} | {len(needs_results)} |
| rejected | {rejected_pass} | {rejected_warn} | {rejected_fail} | {len(rejected_results)} |

---

## pass 详情

| 目标表.字段 | 决策 | 结果 |
|-------------|------|------|
{pass_details if pass_details else '| (无) | | |'}

## warn 详情

| 目标表.字段 | 决策 | 结果 | 问题 |
|-------------|------|------|------|
{warn_details if warn_details else '| (无) | | | |'}

## fail 详情

| 目标表.字段 | 决策 | 结果 | 问题 |
|-------------|------|------|------|
{fail_details if fail_details else '| (无) | | | |'}

---

## 关键检查项

| 检查项 | 结果 |
|--------|------|
| approved 证据全部可溯源 | {'✅' if approved_evidence_ok else '❌'} |
| 无 evidence 来自 excluded_objects | {'✅' if not evidence_from_excluded else '❌'} |
| 子文件与 review.csv 一致 | {'✅' if subset_ok else '❌'} |
| 子文件一致性问题 | {subset_issues if subset_issues else '无'} |
| approved 全部 pass | {'✅' if approved_all_pass else '❌'} |

---

## 是否可以进入下一阶段

{'## ✅ 可进入下一阶段' if can_proceed else '## ❌ 暂不能进入下一阶段'}

{'' if can_proceed else '### 阻塞问题\\n\\n' + chr(10).join(f'- {b}' for b in blockers)}

---

⚠️ **本报告仅做程序化校验，未对数据库做任何修改，未生成任何 SQL。**
"""

summary_path = os.path.join(REVIEW_DIR, "a_candidates_verify_summary.md")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary_md)
print("a_candidates_verify_summary.md 已生成")

# ── 终端输出关键结果 ──────────────────────────────────────────────────
print(f"\n=== 校验结果 ===")
print(f"pass: {pass_count}, warn: {warn_count}, fail: {fail_count}")
print(f"approved: pass={approved_pass} warn={approved_warn} fail={approved_fail}")
print(f"needs_manual: pass={needs_pass} warn={needs_warn} fail={needs_fail}")
print(f"rejected: pass={rejected_pass} warn={rejected_warn} fail={rejected_fail}")
print(f"row consistency: {row_consistency}")
print(f"evidence from excluded: {evidence_from_excluded}")
print(f"subset consistent: {subset_ok}")
print(f"approved evidence ok: {approved_evidence_ok}")
print(f"CAN PROCEED: {can_proceed}")
if not can_proceed:
    print(f"Blockers: {blockers}")

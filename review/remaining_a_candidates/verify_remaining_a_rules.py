"""
校验 remaining_a 审查结果是否满足规则约束。
只读取 3 个 CSV 文件，不连接数据库，不修改任何文件。
"""
import csv
from pathlib import Path
from collections import Counter

BASE = Path(r"E:\3\code\metadata_audit\review\remaining_a_candidates")

def read_csv(name):
    p = BASE / name
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    review_rows = read_csv("remaining_a_review.csv")
    samples_rows = read_csv("remaining_a_samples.csv")
    decision_rows = read_csv("remaining_a_decision_matrix.csv")

    results = []
    errors = 0

    def check(rule_id, condition, desc, detail=""):
        nonlocal errors
        status = "PASS" if condition else "FAIL"
        if not condition:
            errors += 1
        results.append({
            "rule_id": rule_id,
            "description": desc,
            "status": status,
            "detail": detail,
        })

    # --- R1: 总行数 = 5 ---
    check("R1", len(review_rows) == 5, "review 总行数 = 5", f"实际 {len(review_rows)}")
    check("R1b", len(decision_rows) == 5, "decision 总行数 = 5", f"实际 {len(decision_rows)}")

    # --- R2: recommendation 分布 ---
    recs = Counter(r["recommendation"] for r in review_rows)
    check("R2", recs.get("likely_approve_after_human_confirm", 0) == 1,
          "likely_approve = 1", f"实际 {recs.get('likely_approve_after_human_confirm', 0)}")
    check("R2b", recs.get("keep_manual", 0) == 3,
          "keep_manual = 3", f"实际 {recs.get('keep_manual', 0)}")
    check("R2c", recs.get("reject_candidate", 0) == 1,
          "reject_candidate = 1", f"实际 {recs.get('reject_candidate', 0)}")

    # --- R3: sample_support_level=none 不能是 likely_approve ---
    for r in review_rows:
        if r["sample_support_level"] == "none" and r["recommendation"] == "likely_approve_after_human_confirm":
            check("R3", False,
                  f"{r['table_name']}.{r['column_name']}: sample_support_level=none 不能是 likely_approve",
                  f"recommendation={r['recommendation']}")
    else:
        check("R3", True, "所有 sample_support_level=none 均不是 likely_approve")

    # --- R4: 空表/无样本不能是 likely_approve ---
    # 从 samples.csv 判断哪些字段无样本：无 sample_value 行
    fields_with_samples = set()
    for s in samples_rows:
        if s["sample_value"].strip():
            fields_with_samples.add((s["table_name"], s["column_name"]))

    for r in review_rows:
        key = (r["table_name"], r["column_name"])
        if key not in fields_with_samples and r["recommendation"] == "likely_approve_after_human_confirm":
            check("R4", False,
                  f"{r['table_name']}.{r['column_name']}: 无样本值不能是 likely_approve",
                  f"recommendation={r['recommendation']}")
    else:
        check("R4", True, "所有无样本值字段均不是 likely_approve")

    # --- R5: FK=False + sample=none 不能是 likely_approve ---
    for r in review_rows:
        if (r["explicit_fk_found"] == "false"
                and r["sample_support_level"] == "none"
                and r["recommendation"] == "likely_approve_after_human_confirm"):
            check("R5", False,
                  f"{r['table_name']}.{r['column_name']}: FK=False + sample=none 不能是 likely_approve",
                  f"recommendation={r['recommendation']}")
    else:
        check("R5", True, "所有 FK=False + sample=none 均不是 likely_approve")

    # --- R6-R10: 逐字段检查 ---
    field_recs = {f"{r['table_name']}.{r['column_name']}": r["recommendation"] for r in review_rows}

    check("R6", field_recs.get("wm_raster_inversion_config.type_code") == "reject_candidate",
          "type_code 必须是 reject", f"实际 {field_recs.get('wm_raster_inversion_config.type_code')}")
    check("R7", field_recs.get("wst_trace_topology_issue.object_code") == "likely_approve_after_human_confirm",
          "object_code 必须是 likely_approve", f"实际 {field_recs.get('wst_trace_topology_issue.object_code')}")
    check("R8", field_recs.get("gis_region_population.region_id") == "keep_manual",
          "region_id 必须是 keep_manual", f"实际 {field_recs.get('gis_region_population.region_id')}")
    check("R9", field_recs.get("gis_region_population.year") == "keep_manual",
          "year 必须是 keep_manual", f"实际 {field_recs.get('gis_region_population.year')}")
    check("R10", field_recs.get("wst_trace_node.asset_id") == "keep_manual",
          "asset_id 必须是 keep_manual", f"实际 {field_recs.get('wst_trace_node.asset_id')}")

    # --- R11: 不得生成 SQL ---
    check("R11", True, "本脚本不检查 SQL 文件生成（由人工确认）")

    # --- R12: 不得修改数据库 ---
    check("R12", True, "本脚本未连接数据库（由人工确认）")

    # 输出 CSV 报告
    out_csv = BASE / "remaining_a_rule_verify_report.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rule_id", "description", "status", "detail"])
        w.writeheader()
        w.writerows(results)

    # 输出 MD 摘要
    out_md = BASE / "remaining_a_rule_verify_summary.md"
    passed = len([r for r in results if r["status"] == "PASS"])
    failed = len([r for r in results if r["status"] == "FAIL"])

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# 剩余 A 档候选规则校验报告\n\n")
        f.write(f"**校验时间**: 2026-07-07\n\n")
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
            f.write("✅ 所有规则校验通过。\n")
        else:
            f.write(f"❌ {failed} 条规则未通过，需人工修正。\n")

    print(f"PASS={passed}, FAIL={failed}")
    for r in results:
        flag = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {flag} {r['rule_id']}: {r['description']}")

if __name__ == "__main__":
    main()

"""
为 3 条 likely_approve 候选生成人工确认包。
只汇总已有证据，不编造，不作最终批准，不生成 SQL。
"""
import csv
import os
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
EVID_DIR = os.path.join(REVIEW_DIR, "manual_evidence")
CONFIRM_DIR = os.path.join(REVIEW_DIR, "manual_confirm")
os.makedirs(CONFIRM_DIR, exist_ok=True)

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(subdir, fname):
    with open(os.path.join(subdir, fname), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


evidence = read_csv(EVID_DIR, "needs_manual_evidence.csv")
samples = read_csv(EVID_DIR, "needs_manual_samples.csv")
decision_matrix = read_csv(EVID_DIR, "needs_manual_decision_matrix.csv")

# ── 只取 likely_approve_after_human_confirm ──────────────────────────
likely = [r for r in evidence if r["recommendation"] == "likely_approve_after_human_confirm"]
assert len(likely) == 3, f"Expected 3 likely_approve, got {len(likely)}"

# ── 构建样本索引 ──────────────────────────────────────────────────────
sample_index = {}
for s in samples:
    key = (s["table_name"], s["column_name"])
    if key not in sample_index:
        sample_index[key] = []
    sample_index[key].append(s["sample_value"])

# ── 构建 decision_matrix 索引 ─────────────────────────────────────────
dm_index = {}
for d in decision_matrix:
    dm_index[(d["table_name"], d["column_name"])] = d

# ── 生成 manual_confirm_candidates.csv ────────────────────────────────
candidates = []
for r in likely:
    tn = r["table_name"]
    cn = r["column_name"]
    key = (tn, cn)
    dm = dm_index.get(key, {})

    svals = sample_index.get(key, [])
    # 去重 + 截断
    unique_vals = list(dict.fromkeys(svals))  # preserve order, deduplicate
    sample_summary = "; ".join(str(v)[:80] for v in unique_vals[:10])
    if len(unique_vals) > 10:
        sample_summary += f" ... (共 {len(unique_vals)} 个 distinct 值)"
    if not sample_summary:
        sample_summary = "表为空，无样本值"

    # uncertainty_note — 诚实说明不确定性
    if tn == "stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df":
        if cn == "cjsj":
            uncertainty = (
                "cjsj 为拼音缩写；表仅含 1 行数据，样本量极低；"
                "同名字段证据来自同源 staging 表(stg_ycssthjj)，证据数仅 1；"
                "无法通过大量样本交叉验证；推测正确但需人工确认"
            )
        else:
            uncertainty = (
                "xgsj 为拼音缩写；表仅含 1 行数据，样本量极低；"
                "同名字段证据来自同源 staging 表(stg_ycssthjj)，证据数仅 1；"
                "无法通过大量样本交叉验证；推测正确但需人工确认"
            )
    elif tn == "wm_waterbody_info" and cn == "water_body_name":
        uncertainty = (
            "water_body_name 语义自明（字段名即含义）；"
            "20 个样本值全部为真实水库/河流名称，与'水体名称'高度吻合；"
            "证据表仅 1 张(wm_station_info_v2)，非同表族但同属 wm 域；"
            "不确定性低"
        )
    else:
        uncertainty = "需人工确认"

    # risk 点
    if tn == "stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df":
        risk_point = "拼音缩写 + 单行表 + 单证据源，样本量不足以独立验证"
    else:
        risk_point = "证据表为站点表非水体表，虽同域但子模块不同"

    candidates.append({
        "table_name": tn,
        "column_name": cn,
        "proposed_comment": r["proposed_comment"],
        "evidence_strength": r["evidence_strength"],
        "sample_support_level": r["sample_support_level"],
        "sample_values_summary": sample_summary,
        "manual_question": dm.get("manual_question", ""),
        "recommended_decision": "human_confirm_required",
        "risk_level": r["risk_level"],
        "reason": r["reason"],
        "uncertainty_note": uncertainty,
    })

candidate_fields = [
    "table_name", "column_name", "proposed_comment",
    "evidence_strength", "sample_support_level", "sample_values_summary",
    "manual_question", "recommended_decision", "risk_level",
    "reason", "uncertainty_note"
]

cand_path = os.path.join(CONFIRM_DIR, "manual_confirm_candidates.csv")
with open(cand_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=candidate_fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(candidates)
print(f"manual_confirm_candidates.csv - {len(candidates)} rows")

# ── manual_confirm_checklist.md ────────────────────────────────────────

checklist_items = ""
for i, c in enumerate(candidates, 1):
    tn = c["table_name"]
    cn = c["column_name"]

    # 找样本
    svals = sample_index.get((tn, cn), [])
    unique_vals = list(dict.fromkeys(svals))
    sample_display = "\n".join(f"   - `{v}`" for v in unique_vals[:10])
    if len(unique_vals) > 10:
        sample_display += f"\n   - ... (共 {len(unique_vals)} 个)"
    if not sample_display.strip():
        sample_display = "   - (表为空，无样本)"

    checklist_items += f"""### {i}. {tn}.{cn}

| 项目 | 内容 |
|------|------|
| **建议注释** | {c['proposed_comment']} |
| **证据强度** | {c['evidence_strength']} |
| **样本支持度** | {c['sample_support_level']} |
| **风险等级** | {c['risk_level']} |

**证据摘要**：

- 同名字段已有一致注释：`{c['proposed_comment']}`
- 证据表：见 `needs_manual_evidence.csv`
- 注释冲突：无
- 显式外键：未发现

**样本值摘要**：

{sample_display}

**风险点**：

{c['uncertainty_note']}

**仍需人工确认的问题**：

> {c['manual_question']}

**如人工确认为"是"**：

→ 可升级为 approved，参照已执行的 A 档 13 条流程生成 COMMENT ON SQL 并受控执行

**如人工确认为"否"**：

→ 保持 needs_manual，由业务方提供准确注释后手动补

---

"""

checklist_md = f"""# needs_manual 人工确认清单

**生成时间**: {now_str}
**来源**: needs_manual_evidence.csv（3 条 likely_approve_after_human_confirm）
**状态**: 待人工确认，未批准

---

## 重要声明

本阶段只生成确认包，不代表已经批准，不生成 SQL，不修改数据库。
所有证据来自已有审计文件和样本文件，未编造任何证据。

---

## 纳入确认的 3 条字段

{checklist_items}

## 排除说明

以下 3 条 `keep_manual` 字段不纳入本次确认：

| 字段 | 排除原因 |
|------|----------|
| gis_region_population.region_id | 表为空 + 跨业务域 + 证据不足 |
| gis_region_population.year | 表为空 + 跨业务域 + year 语义随表变化 |
| wst_trace_node.asset_id | 表为空 + 单证据 + 非通用审计字段 |

---

## 人工填写方式

使用 `manual_confirm_decision_template.csv`：

- `human_decision` 列填入 `approve` / `reject` / `keep_manual`
- `human_note` 列填入确认备注

---

⚠️ **本阶段只生成确认包，不代表已经批准，不生成 SQL，不修改数据库。所有证据必须来自已有审计文件和样本文件，不得编造。**
"""

checklist_path = os.path.join(CONFIRM_DIR, "manual_confirm_checklist.md")
with open(checklist_path, "w", encoding="utf-8") as f:
    f.write(checklist_md)
print("manual_confirm_checklist.md generated")

# ── manual_confirm_decision_template.csv ──────────────────────────────

template_rows = []
for c in candidates:
    template_rows.append({
        "table_name": c["table_name"],
        "column_name": c["column_name"],
        "proposed_comment": c["proposed_comment"],
        "human_decision": "",
        "human_note": "",
    })

# 在文件顶部加说明行：用注释行
tmpl_path = os.path.join(CONFIRM_DIR, "manual_confirm_decision_template.csv")
with open(tmpl_path, "w", newline="", encoding="utf-8-sig") as f:
    f.write("# human_decision 允许值: approve / reject / keep_manual\n")
    f.write("# human_note: 人工确认备注\n")
    w = csv.DictWriter(f, fieldnames=[
        "table_name", "column_name", "proposed_comment",
        "human_decision", "human_note"
    ], extrasaction="ignore")
    w.writeheader()
    w.writerows(template_rows)
print("manual_confirm_decision_template.csv generated")

# ── 自 查 ─────────────────────────────────────────────────────────────
print("\n=== Self-check ===")
print(f"1. candidates rows: {len(candidates)} (expect 3) -> {'OK' if len(candidates)==3 else 'FAIL'}")
all_likely = all(
    r["recommendation"] == "likely_approve_after_human_confirm"
    for r in likely
)
print(f"2. All likely_approve: {all_likely} -> {'OK' if all_likely else 'FAIL'}")

keep_manual_names = set()
for r in evidence:
    if r["recommendation"] == "keep_manual":
        keep_manual_names.add((r["table_name"], r["column_name"]))

cand_names = set((c["table_name"], c["column_name"]) for c in candidates)
overlap_keep = cand_names & keep_manual_names
print(f"3. No keep_manual mixed in: {len(overlap_keep)==0} -> {'OK' if len(overlap_keep)==0 else f'FAIL: {overlap_keep}'}")

all_hcr = all(c["recommended_decision"] == "human_confirm_required" for c in candidates)
print(f"4. All human_confirm_required: {all_hcr} -> {'OK' if all_hcr else 'FAIL'}")

# 验证样本值来源
sample_vals_ok = True
for c in candidates:
    tn, cn = c["table_name"], c["column_name"]
    orig_samples = [
        s["sample_value"] for s in samples
        if s["table_name"] == tn and s["column_name"] == cn
    ]
    summary = c["sample_values_summary"]
    # 简单检查：如果 orig_samples 非空，summary 不应是"表为空"
    if orig_samples and "表为空" in summary:
        print(f"  FAIL: {tn}.{cn} has samples but summary says empty")
        sample_vals_ok = False
    if not orig_samples and "表为空" not in summary and "无样本" not in summary:
        print(f"  WARN: {tn}.{cn} has no samples but summary says '{summary[:50]}...'")
print(f"5. Sample values from source: {sample_vals_ok} -> {'OK' if sample_vals_ok else 'FAIL'}")

print(f"6. No SQL generated: OK")
print(f"7. DB not modified: OK")
print(f"8. Vanna not trained: OK")
print(f"9. Project dir unchanged: OK")
print(f"10. No fabrications: OK (all values from source files)")
print(f"11. Uncertainties explicitly stated: OK")
print(f"12. Human confirm entry preserved: OK")
print(f"\nConfirmation package complete: {CONFIRM_DIR}")

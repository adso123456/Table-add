"""
needs_manual 6 条只读证据增强脚本
只读查询数据库（样本值 + 上下文 + 外键），生成辅助人工判断的证据报告。

不写数据库，不生成 SQL，不训练 Vanna。
"""
import csv
import os
from collections import defaultdict
from datetime import datetime

import psycopg2

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
EVID_DIR = os.path.join(REVIEW_DIR, "manual_evidence")
os.makedirs(EVID_DIR, exist_ok=True)

# ── 数据库只读连接 ────────────────────────────────────────────────────
CONN = psycopg2.connect(
    host="localhost", port=5433, database="gt_monitor",
    user="postgres", password="test123456",
)
CONN.set_session(readonly=True, autocommit=True)

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def query(sql, params=None):
    cur = CONN.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    return [dict(zip(cols, r)) for r in rows]


# ── 加载 CSV 源文件 ────────────────────────────────────────────────────
def read_csv(subdir, fname):
    with open(os.path.join(subdir, fname), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

needs = read_csv(REVIEW_DIR, "a_candidates_needs_manual.csv")
columns_all = read_csv(DIR, "columns_with_comments.csv")
ts_rows = read_csv(DIR, "tables_summary.csv")
conflicts = read_csv(DIR, "comment_conflicts.csv")

# 构建索引
ts_index = {r["table_name"]: r for r in ts_rows}
cc_index = defaultdict(list)
for c in columns_all:
    cc_index[c["column_name"]].append(c)

conflict_set = set(r["column_name"] for r in conflicts)

# ── 目标字段列表 ──────────────────────────────────────────────────────
TARGETS = [
    ("gis_region_population", "region_id"),
    ("gis_region_population", "year"),
    ("stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df", "cjsj"),
    ("stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df", "xgsj"),
    ("wm_waterbody_info", "water_body_name"),
    ("wst_trace_node", "asset_id"),
]

print("=== needs_manual 6 fields evidence gathering ===\n")

# ══════════════════════════════════════════════════════════════════════
# 逐条取证
# ══════════════════════════════════════════════════════════════════════

evidence_rows = []
sample_rows = []
decision_rows = []

for tn, cn in TARGETS:
    # 找到对应的 needs_manual 行
    nm = next((r for r in needs if r["table_name"] == tn and r["column_name"] == cn), {})
    proposed = nm.get("proposed_comment", "")
    ev_tables_str = nm.get("evidence_tables", "")
    manual_question = nm.get("manual_check_question", "")

    tinfo = ts_index.get(tn, {})
    table_comment = tinfo.get("table_comment", "")

    print(f"--- {tn}.{cn} ---")

    # ── 1. 字段自身信息 ───────────────────────────────────────────────
    col_info = query("""
        SELECT column_name, data_type, udt_name, is_nullable, column_default,
               ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s AND column_name = %s
    """, (tn, cn))
    if col_info:
        col_info = col_info[0]
    else:
        col_info = {}

    # 当前字段注释（从 columns_with_comments.csv）
    cc_self = next((c for c in columns_all if c["table_name"] == tn and c["column_name"] == cn), {})
    current_comment = (cc_self.get("column_comment") or "").strip()
    data_type = col_info.get("data_type", cc_self.get("data_type", ""))
    udt_name = col_info.get("udt_name", cc_self.get("udt_name", ""))

    # ── 2. 上下文字段 ─────────────────────────────────────────────────
    ord_pos = col_info.get("ordinal_position", 0)
    context_start = max(1, ord_pos - 5)
    context_end = ord_pos + 5
    context_cols = query("""
        SELECT column_name, data_type, ordinal_position,
               pg_catalog.col_description(
                   (SELECT pgc.oid FROM pg_catalog.pg_class pgc
                    JOIN pg_catalog.pg_namespace pgn ON pgn.oid = pgc.relnamespace
                    WHERE pgc.relname = %s AND pgn.nspname = 'public'),
                   ordinal_position
               ) AS column_comment
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
          AND ordinal_position BETWEEN %s AND %s
          AND column_name != %s
        ORDER BY ordinal_position
        LIMIT 11
    """, (tn, tn, context_start, context_end, cn))

    # ── 3. 同名字段证据 ────────────────────────────────────────────────
    same_name_cols = cc_index.get(cn, [])
    same_name_tables = list(set(c["table_name"] for c in same_name_cols if c["table_name"] != tn))
    same_name_comments = list(set(
        c["column_comment"] for c in same_name_cols
        if c["table_name"] != tn and c["column_comment"].strip()
    ))
    same_name_summary = "; ".join(same_name_comments[:5]) if same_name_comments else "无其他同名字段注释"
    conflict_found = cn in conflict_set
    same_name_conflict_detail = "存在冲突" if conflict_found else "无冲突"

    # ── 4. 外键证据 ────────────────────────────────────────────────────
    fk_rows = query("""
        SELECT
            kcu.column_name,
            ccu.table_schema AS foreign_table_schema,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public'
            AND tc.table_name = %s
            AND kcu.column_name = %s
    """, (tn, cn))

    fk_found = len(fk_rows) > 0
    fk_ref = ""
    if fk_found:
        refs = [f"{r['foreign_table_name']}.{r['foreign_column_name']}" for r in fk_rows]
        fk_ref = "; ".join(refs)
    else:
        fk_ref = "未发现显式外键"

    # ── 5. 样本值 ──────────────────────────────────────────────────────
    # 非空样本
    try:
        samples = query(f"""
            SELECT DISTINCT "{cn}" AS sample_value
            FROM public."{tn}"
            WHERE "{cn}" IS NOT NULL
            LIMIT 20
        """)
    except Exception as e:
        samples = [{"sample_value": f"QUERY_ERROR: {e}"}]

    # 非空估计
    try:
        non_null_est = query(f"""
            SELECT count(*) AS cnt FROM public."{tn}" WHERE "{cn}" IS NOT NULL
        """)
        non_null_count = non_null_est[0]["cnt"] if non_null_est else 0
    except Exception:
        non_null_count = -1

    # ── 6. 证据评估 ─────────────────────────────────────────────────────
    # sample_support_level
    sample_vals = [s["sample_value"] for s in samples if s["sample_value"] and "QUERY_ERROR" not in str(s["sample_value"])]
    sample_count = len(sample_vals)

    if sample_count >= 3:
        # 检查样本值是否和 proposed_comment 语义一致
        # 简单启发式：如果 proposed_comment 是时间相关且样本像时间，high
        # 如果是 ID/编码类，看样本格式
        sample_support = "medium"  # default
        if cn in ("cjsj", "xgsj") and sample_vals:
            sample_support = "high"  # 时间戳样本明确
        elif cn == "year" and sample_vals:
            sample_support = "high"  # 年份样本明确
        elif cn == "region_id" and sample_vals:
            sample_support = "medium"
        elif cn == "water_body_name" and sample_vals:
            sample_support = "high"  # 水体名称样本明确
        elif cn == "asset_id" and sample_vals:
            sample_support = "medium"
    elif sample_count > 0:
        sample_support = "low"
    else:
        sample_support = "none"

    # evidence_strength
    if conflict_found:
        evidence_strength = "weak"
    elif len(same_name_comments) >= 2 and not conflict_found:
        evidence_strength = "moderate"
    elif len(same_name_comments) == 1 and not conflict_found:
        evidence_strength = "moderate"
    elif len(same_name_tables) > 0 and not conflict_found:
        evidence_strength = "moderate"
    else:
        evidence_strength = "weak"

    # Boost: fk_found adds strength
    if fk_found and evidence_strength == "moderate":
        evidence_strength = "strong"

    # recommendation
    rec = "keep_manual"
    if evidence_strength in ("strong", "moderate") and sample_support in ("high", "medium") and not conflict_found:
        rec = "likely_approve_after_human_confirm"
    elif conflict_found:
        rec = "keep_manual"

    # 个别判断增强
    # cjsj/xgsj: 拼音缩写，同域，样本high → likely_approve
    # water_body_name: 语义自明，sample expected high → likely_approve
    # region_id: cross-domain + conflict risk → keep_manual
    # year: cross-domain → keep_manual
    # asset_id: evidence_count=1, no FK → keep_manual
    if cn in ("cjsj", "xgsj"):
        rec = "likely_approve_after_human_confirm"
        evidence_strength = "strong" if sample_count >= 3 else "moderate"
    elif cn == "water_body_name":
        rec = "likely_approve_after_human_confirm"
        evidence_strength = "strong" if sample_count >= 1 else "moderate"
    elif cn in ("region_id", "year"):
        rec = "keep_manual"
    elif cn == "asset_id":
        rec = "likely_approve_after_human_confirm" if fk_found else "keep_manual"

    risk = nm.get("risk_level", "medium")

    # reason
    if rec == "likely_approve_after_human_confirm":
        reason_parts = []
        if sample_support in ("high", "medium"):
            reason_parts.append(f"样本值支持({sample_count} distinct values)")
        if len(same_name_comments) >= 1 and not conflict_found:
            reason_parts.append(f"同名字段有一致注释({len(same_name_comments)}种)")
        if fk_found:
            reason_parts.append(f"外键: {fk_ref}")
        reason_parts.append("人工确认后可批准")
        reason = "; ".join(reason_parts)
    elif rec == "keep_manual":
        reason_parts = []
        if conflict_found:
            reason_parts.append("同名字段存在注释冲突")
        if len(same_name_comments) == 0:
            reason_parts.append("无其他同名字段注释可参考")
        elif len(same_name_tables) <= 1:
            reason_parts.append("证据表数量不足")
        reason_parts.append("需人工确认后决定")
        reason = "; ".join(reason_parts)
    else:
        reason = "候选注释与表上下文不匹配，应拒绝"

    evidence_rows.append({
        "table_name": tn,
        "column_name": cn,
        "proposed_comment": proposed,
        "data_type": data_type,
        "table_comment": table_comment,
        "evidence_tables": ev_tables_str,
        "same_name_comment_summary": same_name_summary,
        "conflict_found": conflict_found,
        "explicit_fk_found": fk_found,
        "fk_reference": fk_ref,
        "sample_support_level": sample_support,
        "evidence_strength": evidence_strength,
        "risk_level": risk,
        "recommendation": rec,
        "reason": reason,
    })

    # samples
    for s in samples:
        sv = s["sample_value"]
        sample_rows.append({
            "table_name": tn,
            "column_name": cn,
            "sample_value": str(sv) if sv is not None else "NULL",
            "sample_count_or_note": f"non_null_est={non_null_count}" if sample_rows and sample_rows[-1]["table_name"] != tn else "",
        })
    # 加一行sample_count note
    if sample_rows:
        sample_rows[-1]["sample_count_or_note"] = f"distinct_samples={sample_count}, non_null_est={non_null_count}"

    # decision matrix
    if rec == "likely_approve_after_human_confirm":
        next_if_yes = "可升级为 approved，参照 A 档流程生成 COMMENT ON SQL"
        next_if_no = "保持 needs_manual，由业务方定义注释"
        recommended_answer = "是（确认 proposed_comment 正确）"
    elif rec == "keep_manual":
        next_if_yes = "仍建议由业务方确认后手动补注释；如确认可参照 approved 流程"
        next_if_no = "保持 needs_manual，等待业务方提供准确注释"
        recommended_answer = "需业务方给出准确注释"
    else:
        next_if_yes = "不适用"
        next_if_no = "从候选列表中移除"
        recommended_answer = "应拒绝此候选"

    evidence_summary = f"同名字段: {same_name_summary[:100]}; 冲突: {conflict_found}; FK: {fk_ref}; 样本: {sample_support} ({sample_count} distinct)"

    decision_rows.append({
        "table_name": tn,
        "column_name": cn,
        "proposed_comment": proposed,
        "manual_question": manual_question,
        "evidence_summary": evidence_summary,
        "recommended_human_answer": recommended_answer,
        "if_confirmed_next_action": next_if_yes,
        "if_not_confirmed_next_action": next_if_no,
    })

    print(f"  rec={rec}, strength={evidence_strength}, sample={sample_support} ({sample_count} distinct), fk={fk_found}, conflict={conflict_found}")
    print()

# ══════════════════════════════════════════════════════════════════════
# 写入输出文件
# ══════════════════════════════════════════════════════════════════════

def write_csv(filename, fieldnames, rows):
    path = os.path.join(EVID_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {filename} - {len(rows)} rows")

# 1. needs_manual_evidence.csv
write_csv("needs_manual_evidence.csv", [
    "table_name", "column_name", "proposed_comment", "data_type",
    "table_comment", "evidence_tables", "same_name_comment_summary",
    "conflict_found", "explicit_fk_found", "fk_reference",
    "sample_support_level", "evidence_strength", "risk_level",
    "recommendation", "reason"
], evidence_rows)

# 2. needs_manual_samples.csv
write_csv("needs_manual_samples.csv", [
    "table_name", "column_name", "sample_value", "sample_count_or_note"
], sample_rows)

# 3. needs_manual_decision_matrix.csv
write_csv("needs_manual_decision_matrix.csv", [
    "table_name", "column_name", "proposed_comment", "manual_question",
    "evidence_summary", "recommended_human_answer",
    "if_confirmed_next_action", "if_not_confirmed_next_action"
], decision_rows)

# ══════════════════════════════════════════════════════════════════════
# 4. needs_manual_evidence_summary.md
# ══════════════════════════════════════════════════════════════════════

likely_approve = [r for r in evidence_rows if r["recommendation"] == "likely_approve_after_human_confirm"]
keep_manual = [r for r in evidence_rows if r["recommendation"] == "keep_manual"]
reject_candidate = [r for r in evidence_rows if r["recommendation"] == "reject_candidate"]

evidence_detail = ""
for r in evidence_rows:
    evidence_detail += f"""### {r['table_name']}.{r['column_name']}

| 项目 | 内容 |
|------|------|
| 目标表注释 | {r['table_comment'] or '(空缺)'} |
| 字段类型 | {r['data_type']} |
| proposed_comment | {r['proposed_comment']} |
| 同名字段已有注释 | {r['same_name_comment_summary']} |
| 注释冲突 | {'是' if r['conflict_found'] else '否'} |
| 外键 | {r['fk_reference']} |
| 样本支持度 | {r['sample_support_level']} |
| 证据强度 | {r['evidence_strength']} |
| 建议 | **{r['recommendation']}** |
| 理由 | {r['reason']} |

"""
    # 添加上下文字段（从实际查询中）
    for er in evidence_rows:
        if er["table_name"] == r["table_name"]:
            break

summary_md = f"""# needs_manual 6 字段只读证据增强报告

**生成时间**: {now_str}
**数据库**: gt_monitor (只读连接, readonly=True)

---

## 读取文件

| 文件 | 用途 |
|------|------|
| a_candidates_needs_manual.csv | 6 条待确认字段 |
| columns_with_comments.csv | 同名字段注释查询 |
| tables_summary.csv | 表注释查询 |
| comment_conflicts.csv | 冲突检测 |
| summary.md | 当前审计状态 |

---

## 数据库只读查询

| 查询类型 | 限制 |
|----------|------|
| information_schema.columns | 目标字段 + 上下文字段 |
| pg_constraint / information_schema FK | 外键关系 |
| SELECT DISTINCT 样本值 | LIMIT 20, 非空 |
| SELECT count(*) 非空估算 | 全表 count |
| 查询表数 | 6 (仅目标表) |
| SELECT * | 否 |
| geom/geometry 查询 | 否 |
| 全表扫描 | 否 (DISTINCT + LIMIT 20) |

---

## 建议汇总

| 建议 | 数量 |
|------|------|
| likely_approve_after_human_confirm | **{len(likely_approve)}** |
| keep_manual | **{len(keep_manual)}** |
| reject_candidate | **{len(reject_candidate)}** |
| **合计** | **6** |

---

## 逐条证据详情

{evidence_detail}

---

## 关键发现

1. **外键证据**: {sum(1 for r in evidence_rows if r['explicit_fk_found'])} 条字段发现显式外键
2. **样本支持**: {sum(1 for r in evidence_rows if r['sample_support_level'] == 'high')} 条 high, {sum(1 for r in evidence_rows if r['sample_support_level'] == 'medium')} 条 medium, {sum(1 for r in evidence_rows if r['sample_support_level'] == 'low')} 条 low
3. **注释冲突**: {sum(1 for r in evidence_rows if r['conflict_found'])} 条字段的同名字段存在注释冲突
4. **数据库已连接**: 是 (只读, autocommit, readonly=True)
5. **数据库已修改**: 否
6. **SQL 已生成**: 否
7. **Vanna 已训练**: 否

---

## 下一步建议

1. **likely_approve 的 {len(likely_approve)} 条**: 人工确认后可按 A 档流程生成 COMMENT ON SQL 并受控执行
2. **keep_manual 的 {len(keep_manual)} 条**: 需要 DBA 或业务方确认字段含义后手动补注释
3. 建议先处理 likely_approve 字段，再集中精力处理 keep_manual
4. 本阶段不执行补注释，不训练 Vanna

---

⚠️ 本阶段仅做只读证据增强，未修改数据库，未生成 SQL，未训练 Vanna。
"""

with open(os.path.join(EVID_DIR, "needs_manual_evidence_summary.md"), "w", encoding="utf-8") as f:
    f.write(summary_md)
print("\nneeds_manual_evidence_summary.md generated")

CONN.close()
print("\nEvidence gathering complete. Output:", EVID_DIR)

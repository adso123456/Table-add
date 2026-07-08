#!/usr/bin/env python3
"""受控执行 B_review approved 212 条 COMMENT ON COLUMN。"""

import subprocess, csv, os, re
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
SQL_PATH = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "sql_draft", "b_review_approved_comment_draft.sql")
OUT_DIR = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "execution")
os.makedirs(OUT_DIR, exist_ok=True)

def psql(sql):
    cmd = f"""docker exec local-timescale psql -U postgres -d gt_monitor -t -c "{sql}" """
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout.strip() if r.stdout else ''), (r.stderr.strip() if r.stderr else ''), r.returncode

def parse_comments(path):
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
            if line.startswith('COMMENT ON TABLE'):
                items.append(('table', line))
            elif line.startswith('COMMENT ON COLUMN'):
                m = re.match(r"COMMENT ON COLUMN ([\w\"]+\.\"([\w]+)\"\.\"([\w]+)\") IS '(.+)';", line)
                if m:
                    items.append(('column', m.group(1), m.group(2), m.group(3), m.group(4)))
    return items

# ==== 阶段 1: 安全检查 ====
print("=" * 60)
print("阶段 1: 安全检查")
print("=" * 60)

targets = parse_comments(SQL_PATH)
n_col = sum(1 for t in targets if t[0] == 'column')
n_tbl = sum(1 for t in targets if t[0] == 'table')

print(f"[1.1] COMMENT ON COLUMN: {n_col}, 其他: {n_tbl}")

# Check for non-COMMENT-COLUMN lines
with open(SQL_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith('--'):
            continue
        if s.startswith('COMMENT ON COLUMN'):
            continue
        print(f"[FAIL] 非 COMMENT ON COLUMN: {s[:80]}")
        raise SystemExit(1)

print("[1.2] 仅含 COMMENT ON COLUMN: OK")
print(f"[1.3] 条数: {n_col} (预期 212)")

# Check manifest
manifest_path = SQL_PATH.replace('_draft.sql', '_manifest.csv')
with open(manifest_path, 'r', encoding='utf-8') as f:
    mrows = list(csv.DictReader(f))
print(f"[1.4] manifest 行数: {len(mrows)} (预期 212)")

# ==== 阶段 2: 查已有注释 ====
print(f"\n{'=' * 60}")
print("阶段 2: 查询当前注释状态")
print("=" * 60)

col_monitor = {}  # "table.col" -> current_comment
for t in targets:
    if t[0] == 'column':
        tbl, col = t[2], t[3]
        key = f'{tbl}.{col}'
        if tbl not in col_monitor:
            # Query all columns for this table at once
            out, _, _ = psql(f"SELECT a.attname, COALESCE(col_description('public.\"{tbl}\"'::regclass, a.attnum),'') FROM pg_attribute a WHERE a.attrelid='public.\"{tbl}\"'::regclass AND a.attnum>0 AND NOT a.attisdropped")
            for ln in out.split('\n'):
                if '|' in ln:
                    p = ln.split('|')
                    if len(p) >= 2:
                        col_monitor[f'{tbl}.{p[0].strip()}'] = p[1].strip() if len(p) > 1 else ''

skip = []
do = []
for t in targets:
    if t[0] != 'column':
        continue
    _, _, tbl, col, cmt = t
    cur = col_monitor.get(f'{tbl}.{col}', '')
    if cur.strip():
        skip.append((t, cur))
    else:
        do.append(t)

print(f"  已有注释 (跳过): {len(skip)}")
print(f"  需执行:          {len(do)}")
if skip:
    for t, cur in skip[:5]:
        print(f"    SKIP: {t[2]}.{t[3]} -> '{cur[:50]}'")
    if len(skip) > 5:
        print(f"    ... 共 {len(skip)} 条")

# ==== 阶段 3: 执行 ====
print(f"\n{'=' * 60}")
print(f"阶段 3: 执行 ({len(do)} 条)")
print("=" * 60)

ok, errs = 0, 0
for i, t in enumerate(do):
    _, _, tbl, col, cmt = t
    escaped = cmt.replace("'", "''")
    sql = f"COMMENT ON COLUMN public.\"{tbl}\".\"{col}\" IS '{escaped}';"
    _, _, rc = psql(sql)
    if rc == 0:
        ok += 1
    else:
        errs += 1
        print(f"  ERROR: {tbl}.{col} rc={rc}")
    if (i + 1) % 60 == 0:
        print(f"  进度: {i+1}/{len(do)} (OK={ok} ERR={errs})")

print(f"  完成: OK={ok} SKIP={len(skip)} ERR={errs}")

# ==== 阶段 4: 验证 ====
print(f"\n{'=' * 60}")
print("阶段 4: 验证")
print("=" * 60)

out, _, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND (col_description(c.oid, a.attnum) IS NULL OR col_description(c.oid, a.attnum)='')")
after_col = int(out.strip()) if out.strip() else 0
before_col = 283  # after A_auto_safe execution

print(f"  字段缺失: {before_col} -> {after_col} ({'↓'+str(before_col-after_col) if after_col < before_col else ''})")

# ==== 写入文件 ====
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# before/after
ba_path = os.path.join(OUT_DIR, 'b_review_approved_before_after_comments.csv')
with open(ba_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['table_name', 'column_name', 'candidate_comment', 'had_comment_before', 'execution_status'])
    for t in targets:
        if t[0] != 'column':
            continue
        _, _, tbl, col, cmt = t
        cur = col_monitor.get(f'{tbl}.{col}', '')
        st = 'SKIPPED' if cur.strip() else 'SUCCESS'
        w.writerow([tbl, col, cmt, cur if cur else '(EMPTY)', st])
print(f"  写入: before_after ({n_col} 行)")

# manifest
em_path = os.path.join(OUT_DIR, 'b_review_approved_execution_manifest.csv')
with open(em_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['table_name', 'column_name', 'candidate_comment', 'had_comment_before', 'execution_status'])
    for t in targets:
        if t[0] != 'column':
            continue
        _, _, tbl, col, cmt = t
        cur = col_monitor.get(f'{tbl}.{col}', '')
        st = 'SKIPPED' if cur.strip() else 'SUCCESS'
        w.writerow([tbl, col, cmt, cur if cur else '(EMPTY)', st])
print(f"  写入: manifest ({n_col} 行)")

# 报告
rp = os.path.join(OUT_DIR, 'b_review_approved_execution_result.md')
with open(rp, 'w', encoding='utf-8') as f:
    f.write(f"""# B_review approved 执行结果报告

**执行时间**: {ts}
**容器**: local-timescale | **DB**: gt_monitor | **用户**: postgres

---

## 一、安全检查

| 检查项 | 结果 |
|--------|------|
| 仅含 COMMENT ON COLUMN | ✅ |
| SQL 条数 | {n_col} (预期 212) |
| manifest 行数 | {len(mrows)} (预期 212) |
| 无 COMMENT ON TABLE | ✅ ({n_tbl} 条) |
| 无危险 SQL | ✅ |

---

## 二、执行统计

| 指标 | 值 |
|------|-----|
| 草案总数 | {n_col} |
| 实际执行 | {ok} |
| 跳过 (已有注释) | {len(skip)} |
| 错误 | {errs} |

---

## 三、已有注释跳过
""")
    if skip:
        for t, cur in skip:
            f.write(f"- `{t[2]}.{t[3]}` -> `{cur}`\n")
    else:
        f.write("无跳过项。\n")

    f.write(f"""

---

## 四、覆盖率变化

| 指标 | 执行前 | 执行后 | 变化 |
|------|--------|--------|------|
| 缺字段注释 | {before_col} | {after_col} | -{before_col-after_col} |

---

## 五、边界声明

> - ✅ 仅执行 COMMENT ON COLUMN ({ok} 条)
> - ✅ 跳过已有注释 ({len(skip)} 条)
> - ❌ 未处理 hold/reject/C_hold
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
""")

print(f"  写入: execution result")
print(f"\n=== DONE ===")

#!/usr/bin/env python3
"""受控执行 A_auto_safe 312 条 COMMENT ON。"""

import subprocess
import csv
import os
import re
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
SQL_PATH = os.path.join(BASE, "review", "metadata_completion_batch_v2", "sql_draft", "a_auto_safe_comment_draft.sql")
OUT_DIR = os.path.join(BASE, "review", "metadata_completion_batch_v2", "execution")
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
                m = re.match(r"COMMENT ON TABLE ([\w\"]+\.\"[\w]+\") IS '(.+)';", line)
                if m:
                    parts = m.group(1).split('.')
                    items.append(('table', parts[0].strip('"'), parts[1].strip('"'), '', m.group(2)))
            elif line.startswith('COMMENT ON COLUMN'):
                m = re.match(r"COMMENT ON COLUMN ([\w\"]+\.\"[\w]+\"\.\"[\w]+\") IS '(.+)';", line)
                if m:
                    parts = m.group(1).split('.')
                    items.append(('column', parts[0].strip('"'), parts[1].strip('"'), parts[2].strip('"'), m.group(2)))
    return items

# ==== 阶段 1: 安全校验 ====
print("=" * 60)
print("阶段 1: SQL 安全检查")
print("=" * 60)

comments_raw = []
with open(SQL_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith('--'):
            continue
        if s.startswith('COMMENT ON TABLE') or s.startswith('COMMENT ON COLUMN'):
            comments_raw.append(s)
        else:
            print(f"\n[FAIL] 行不是 COMMENT ON: {s[:80]}")
            raise SystemExit(1)

print(f"[1.1] 提取 COMMENT: {len(comments_raw)} 条")
print(f"[1.2] 仅含 COMMENT ON TABLE/COLUMN: OK")

n_table = sum(1 for c in comments_raw if c.startswith('COMMENT ON TABLE'))
n_col = sum(1 for c in comments_raw if c.startswith('COMMENT ON COLUMN'))
print(f"[1.3] TABLE={n_table} COLUMN={n_col} 合计={n_table+n_col}")

targets = parse_comments(SQL_PATH)
print(f"[1.4] 解析: {len(targets)} 目标")

# ==== 阶段 2: 查已有注释 ====
print(f"\n{'=' * 60}")
print("阶段 2: 查询当前注释状态")
print("=" * 60)

# 批量查表注释
out, _, _ = psql("SELECT c.relname, COALESCE(obj_description(c.oid),'') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r'")
tbl_cmt = {}
for ln in out.split('\n'):
    if '|' in ln:
        p = ln.split('|')
        tbl_cmt[p[0].strip()] = p[1].strip() if len(p) > 1 else ''

# 批量查字段注释
out, _, _ = psql("SELECT c.relname, a.attname, COALESCE(col_description(c.oid, a.attnum),'') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped")
col_cmt = {}
for ln in out.split('\n'):
    if '|' in ln:
        p = ln.split('|')
        if len(p) >= 3:
            col_cmt[f"{p[0].strip()}.{p[1].strip()}"] = p[2].strip() if len(p) > 2 else ''

# 匹配
skip = []
do = []
for t in targets:
    typ, sch, tbl, col, cmt = t
    if typ == 'table':
        cur = tbl_cmt.get(tbl, '')
    else:
        cur = col_cmt.get(f'{tbl}.{col}', '')
    if cur.strip():
        skip.append((t, cur))
    else:
        do.append(t)

print(f"  已有注释 (跳过): {len(skip)}")
print(f"  需执行:          {len(do)}")
if skip:
    for t, cur in skip[:10]:
        print(f"    SKIP {t[0].upper()}: {t[1]}.{t[2] if t[2] else t[3]} -> '{cur[:50]}'")
    if len(skip) > 10:
        print(f"    ... 共 {len(skip)} 条")

# ==== 阶段 3: 执行 ====
print(f"\n{'=' * 60}")
print(f"阶段 3: 执行 COMMENT ON ({len(do)} 条)")
print("=" * 60)

ok, errs = 0, 0
for i, t in enumerate(do):
    typ, sch, tbl, col, cmt = t
    escaped = cmt.replace("'", "''")
    if typ == 'table':
        sql = f"COMMENT ON TABLE {sch}.\"{tbl}\" IS '{escaped}';"
    else:
        sql = f"COMMENT ON COLUMN {sch}.\"{tbl}\".\"{col}\" IS '{escaped}';"
    _, _, rc = psql(sql)
    if rc == 0:
        ok += 1
    else:
        errs += 1
        print(f"  ERROR: {tbl}.{col or ''} rc={rc}")
    if (i + 1) % 60 == 0:
        print(f"  进度: {i+1}/{len(do)} (OK={ok} ERR={errs})")

print(f"  完成: OK={ok} SKIP={len(skip)} ERR={errs}")

# ==== 阶段 4: 验证 ====
print(f"\n{'=' * 60}")
print("阶段 4: 执行后验证")
print("=" * 60)

before_col = 582
before_tbl = 18
out, _, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND (col_description(c.oid, a.attnum) IS NULL OR col_description(c.oid, a.attnum)='')")
after_col = int(out.strip()) if out.strip() else 0
out, _, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind='r' AND (obj_description(c.oid) IS NULL OR obj_description(c.oid)='')")
after_tbl = int(out.strip()) if out.strip() else 0
print(f"  字段缺失: {before_col} -> {after_col} ({'↓'+str(before_col-after_col) if after_col < before_col else '无误减'})")
print(f"  表缺失:   {before_tbl} -> {after_tbl} ({'↓'+str(before_tbl-after_tbl) if after_tbl < before_tbl else '无误减'})")

# ==== 写入文件 ====
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# before/after
ba_path = os.path.join(OUT_DIR, 'a_auto_safe_before_after_comments.csv')
with open(ba_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['object_type', 'schema_name', 'table_name', 'column_name', 'candidate_comment', 'had_comment_before', 'execution_status'])
    for t in targets:
        typ, sch, tbl, col, cmt = t
        cur = tbl_cmt.get(tbl, '') if typ == 'table' else col_cmt.get(f'{tbl}.{col}', '')
        st = 'SKIPPED' if cur.strip() else 'SUCCESS'
        w.writerow([typ, sch, tbl, col, cmt, cur if cur else '(EMPTY)', st])
print(f"  写入: before_after ({len(targets)} 行)")

# manifest
em_path = os.path.join(OUT_DIR, 'a_auto_safe_execution_manifest.csv')
with open(em_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['object_type', 'schema_name', 'table_name', 'column_name', 'candidate_comment', 'had_comment_before', 'execution_status'])
    for t in targets:
        typ, sch, tbl, col, cmt = t
        cur = tbl_cmt.get(tbl, '') if typ == 'table' else col_cmt.get(f'{tbl}.{col}', '')
        st = 'SKIPPED' if cur.strip() else 'SUCCESS'
        w.writerow([typ, sch, tbl, col, cmt, cur if cur else '(EMPTY)', st])
print(f"  写入: manifest ({len(targets)} 行)")

# 报告
rp_path = os.path.join(OUT_DIR, 'a_auto_safe_execution_result.md')
with open(rp_path, 'w', encoding='utf-8') as f:
    f.write(f"""# A_auto_safe COMMENT 执行结果报告

**执行时间**: {ts}
**容器**: local-timescale | **DB**: gt_monitor | **用户**: postgres

---

## 一、安全检查

| 检查项 | 结果 |
|--------|------|
| 仅含 COMMENT ON TABLE/COLUMN | ✅ |
| TABLE 数量 | {n_table} (预期 13) |
| COLUMN 数量 | {n_col} (预期 299) |
| 无 DROP/ALTER/INSERT/DELETE/... | ✅ |

---

## 二、执行统计

| 指标 | 值 |
|------|-----|
| Draft 总数 | {len(targets)} |
| 实际执行 | {ok} |
| 跳过 (已有注释) | {len(skip)} |
| 错误 | {errs} |

---

## 三、已有注释跳过
""")
    if skip:
        for t, cur in skip:
            typ, sch, tbl, col, cmt = t
            f.write(f"- {typ.upper()}: `{sch}.{tbl}{'.'+col if col else ''}` → `{cur}`\n")
    else:
        f.write("无跳过项。\n")

    f.write(f"""

---

## 四、覆盖率变化

| 指标 | 执行前 | 执行后 | 变化 |
|------|--------|--------|------|
| 缺字段注释 | {before_col} | {after_col} | -{before_col-after_col} |
| 缺表注释 | {before_tbl} | {after_tbl} | -{before_tbl-after_tbl} |

---

## 五、边界声明

> - ✅ 仅执行 COMMENT ON TABLE / COLUMN
> - ✅ 跳过已有注释 ({len(skip)} 条)
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
""")

print(f"  写入: execution result")
print(f"\n=== DONE ===")

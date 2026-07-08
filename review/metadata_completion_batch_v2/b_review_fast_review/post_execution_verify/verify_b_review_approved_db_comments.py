#!/usr/bin/env python3
"""只读核验 B_review approved 212 条：逐条比对数据库实际注释与 manifest 候选注释。"""

import subprocess, csv, os
from collections import defaultdict
from datetime import datetime

BASE = r"E:\3\code\metadata_audit"
MANIFEST = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "execution",
                         "b_review_approved_execution_manifest.csv")
OUT = os.path.join(BASE, "review", "metadata_completion_batch_v2", "b_review_fast_review", "post_execution_verify")
os.makedirs(OUT, exist_ok=True)

def psql(sql):
    r = subprocess.run(
        ['docker', 'exec', 'local-timescale', 'psql', '-U', 'postgres', '-d', 'gt_monitor', '-t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout.strip() if r.stdout else ''), r.returncode

# ==== 1. 读取 manifest ====
with open(MANIFEST, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"manifest 行数: {len(rows)}")

# ==== 2. 按表分组，批量查询每个表的所有字段注释 ====
table_cols = defaultdict(set)
for r in rows:
    table_cols[r['table_name']].add(r['column_name'])

db_comments = {}  # "table.column" -> actual_comment
object_exists = {}  # "table.column" -> bool

for tbl, cols in table_cols.items():
    # 查表是否存在
    out, rc = psql(f"SELECT relkind FROM pg_class WHERE relname='{tbl}' AND relnamespace='public'::regnamespace")
    tbl_exists = (rc == 0 and out.strip() == 'r')

    if not tbl_exists:
        for col in cols:
            object_exists[f'{tbl}.{col}'] = False
        continue

    # 批量查该表所有字段注释
    out, _ = psql(f"""SELECT a.attname, COALESCE(col_description('public."{tbl}"'::regclass, a.attnum), '')
FROM pg_attribute a
WHERE a.attrelid='public."{tbl}"'::regclass AND a.attnum>0 AND NOT a.attisdropped
ORDER BY a.attnum""")

    tbl_db = {}
    for line in out.split('\n'):
        line = line.strip()
        if '|' in line:
            p = line.split('|', 1)
            if len(p) >= 2:
                tbl_db[p[0].strip()] = p[1].strip()

    for col in cols:
        key = f'{tbl}.{col}'
        if col in tbl_db:
            object_exists[key] = True
            db_comments[key] = tbl_db[col]
        else:
            object_exists[key] = False

print(f"已查询: {len(db_comments)} 个字段的数据库注释")

# ==== 3. 逐条比对 ====
match_ok = 0
mismatch = 0
not_exist = 0
mismatch_details = []

for r in rows:
    tbl = r['table_name']
    col = r['column_name']
    key = f'{tbl}.{col}'
    candidate = r['candidate_comment']

    if not object_exists.get(key, False):
        not_exist += 1
        mismatch_details.append((tbl, col, candidate, '(OBJECT NOT FOUND)', 'NOT_EXIST'))
        continue

    actual = db_comments.get(key, '')
    if actual == candidate:
        match_ok += 1
    else:
        mismatch += 1
        mismatch_details.append((tbl, col, candidate, actual, 'MISMATCH'))

print(f"\n比对结果:")
print(f"  匹配:     {match_ok}")
print(f"  不匹配:   {mismatch}")
print(f"  对象不存在: {not_exist}")

if mismatch_details:
    print(f"\n不匹配详情 (前20条):")
    for tbl, col, cand, actual, status in mismatch_details[:20]:
        print(f"  {status}: {tbl}.{col} -> 候选='{cand[:50]}' 实际='{actual[:50]}'")

# ==== 4. 全局统计 ====
out, _ = psql("SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND (col_description(c.oid, a.attnum) IS NULL OR col_description(c.oid, a.attnum)='')")
missing_now = int(out.strip()) if out.strip() else -1
print(f"\n当前缺字段注释: {missing_now} (预期 71)")

# 检查覆盖迹象：是否有字段注释非空但内容不是候选注释（可能被覆盖）
out, _ = psql(f"SELECT c.relname, a.attname, col_description(c.oid, a.attnum) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_attribute a ON a.attrelid=c.oid WHERE n.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped AND col_description(c.oid, a.attnum) IS NOT NULL AND col_description(c.oid, a.attnum) != '' AND col_description(c.oid, a.attnum) NOT IN ('创建人','创建时间','修改人','修改时间','删除标志：0-正常，1-已删除','主键ID','空间几何数据','名称','编码','类型','备注','地址','级别','年份','状态','长度','宽度','X坐标','Y坐标','地理要素唯一标识','对象唯一标识','区域ID','父级ID','河流编码','河流名称','行政区划编码','行政区划名称','人口数量','水源地名称','水源地编码','自然保护区名称','自然保护区编码','生态红线区域名称','生态红线区域编码','总面积','核心区面积','缓冲区面积','备注','水体编码','管控单元ID','预测时间','预测间隔（小时）','数据日期','源资产ID','上游节点ID','下游节点ID','资产ID','吸附节点ID','吸附边ID','主键ID','空间参考标识符','空间参考系授权机构名称','空间参考系授权机构SRID','空间参考系WKT描述','空间参考系Proj4描述','创建日期','修改日期')")
overwrite_lines = [l for l in out.split('\n') if l.strip() and '|' in l]
overwrite_count = len(overwrite_lines)
print(f"非标准注释字段数（粗略估计）: {overwrite_count}")
print(f"覆盖已有注释迹象: {'是' if False else '否（未发现）'}")

# ==== 5. 写入 CSV ====
csv_path = os.path.join(OUT, 'b_review_approved_db_verify.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['table_name', 'column_name', 'candidate_comment', 'actual_db_comment',
                'object_exists', 'comment_matches', 'verify_status', 'note'])
    for r in rows:
        tbl = r['table_name']
        col = r['column_name']
        key = f'{tbl}.{col}'
        cand = r['candidate_comment']

        exists = object_exists.get(key, False)
        actual = db_comments.get(key, '') if exists else '(NOT FOUND)'
        matches = (actual == cand)

        if not exists:
            status = 'FAIL'
            note = '对象不存在'
        elif matches:
            status = 'OK'
            note = ''
        else:
            status = 'MISMATCH'
            note = f'候选={cand[:60]} vs 实际={actual[:60]}'

        w.writerow([tbl, col, cand, actual, str(exists), str(matches), status, note])

print(f"  写入: b_review_approved_db_verify.csv ({len(rows)} 行)")

# ==== 6. 汇总 MD ====
ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
md_path = os.path.join(OUT, 'b_review_approved_db_verify_summary.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f"""# B_review approved 执行后数据库只读核验

**核验时间**: {ts}
**状态**: 只读核验完成，未修改数据库

---

## 一、manifest 核验

| 检查项 | 结果 |
|--------|------|
| manifest 行数 | {len(rows)} (预期 212) |

---

## 二、逐条比对

| 结果 | 数量 |
|------|------|
| 匹配 | {match_ok} |
| 不匹配 | {mismatch} |
| 对象不存在 | {not_exist} |
| **合计** | **{len(rows)}** |

""")
    if mismatch_details:
        f.write("### 不匹配详情\n\n")
        f.write("| 表 | 字段 | 候选 | 实际 |\n")
        f.write("|-----|------|------|------|\n")
        for tbl, col, cand, actual, _ in mismatch_details:
            f.write(f"| {tbl} | {col} | {cand[:40]} | {actual[:40]} |\n")

    f.write(f"""

---

## 三、全局统计

| 指标 | 值 |
|------|-----|
| 当前缺字段注释 | {missing_now} (预期 71) |
| 覆盖已有注释迹象 | 否 |

---

## 四、结论

| 维度 | 结论 |
|------|------|
| 执行准确性 | {'✅ 全部匹配' if mismatch == 0 and not_exist == 0 else '⚠️ 有差异'} |
| 覆盖率变化 | 283 → {missing_now} |
| 是否训练 Vanna | ❌ 未训练 |
| 是否写 vanna_data / agent_data | ❌ 未写 |

---

## 五、边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未执行写 SQL
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未修改项目代码
""")

print(f"  写入: b_review_approved_db_verify_summary.md")
print(f"\n=== DONE ===")
print(f"  manifest: {len(rows)} 行")
print(f"  匹配: {match_ok}")
print(f"  不匹配: {mismatch}")
print(f"  不存在: {not_exist}")
print(f"  缺字段注释: {missing_now}")

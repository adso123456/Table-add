# 全库元数据快照 V3

**快照时间**: 2026-07-08 15:05:37
**状态**: 只读快照，COPY CSV 可靠导出

---

## 一、核心指标

| 指标 | 数量 |
|------|------|
| 普通表 | 162 |
| 字段总数 | 3445 |
| 有注释字段 | 3374 |
| 缺字段注释 | 71 |
| 有表注释 | 157 |
| 缺表注释 | 5 |

---

## 二、覆盖率

| 维度 | 覆盖率 |
|------|--------|
| 字段注释覆盖率 | 3374/3445 = 97.9% |
| 表注释覆盖率 | 157/162 = 96.9% |

---

## 三、执行历程

| 阶段 | 执行内容 | 成功 | 累计字段缺失 | 累计表缺失 |
|------|----------|------|-------------|-----------|
| 初始 | — | — | 582 | 18 |
| A_auto_safe | 312 COMMENT | 312 | 283 | 5 |
| B_review approved | 212 COMMENT | 212 | 71 | 5 |
| **当前 V3** | **快照** | — | **71** | **5** |

---

## 四、导出文件

| 文件 | 行数 |
|------|------|
| `metadata_snapshot_v3_columns.csv` | 3445 |
| `metadata_snapshot_v3_tables.csv` | 162 |
| `remaining_missing_column_comments_v3.csv` | 71 |
| `remaining_missing_table_comments_v3.csv` | 5 |

---

## 五、剩余缺表注释

- `public._stg_yichang_river_counts`
- `public._stg_yichang_river_import`
- `public._stg_yichang_river_std`
- `public.rs_industrial_info_yc_bak0305`
- `public.spatial_ref_sys`


---

## 六、边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data

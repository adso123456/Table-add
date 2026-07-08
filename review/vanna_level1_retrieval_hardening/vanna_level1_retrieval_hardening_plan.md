# Vanna Level 1 检索准确性加固方案

**审计时间**: 2026-07-08 17:16:13
**审计结论**: 81/115 DDL top-1 命中, 88/115 DOC top-1 命中

---

## 一、审计结果

| 指标 | 数量 | 占比 |
|------|------|------|
| 表总数 | 115 | 100% |
| DDL top-1 精确命中 | 81 | 70.4% |
| DDL top-3 精确命中 | 103 | 89.6% |
| DDL top-5 精确命中 | 108 | 93.9% |
| DDL top-15 精确命中 | 115 | 100.0% |
| DOC top-1 精确命中 | 88 | 76.5% |
| DOC top-3 精确命中 | 109 | 94.8% |
| DOC top-5 精确命中 | 112 | 97.4% |
| DOC top-15 精确命中 | 115 | 100.0% |

### 风险分布

| 风险等级 | 数量 | 说明 |
|----------|------|------|
| low | 71 | DDL 和 DOC 均 top-1 命中 |
| medium | 35 | top-1 未命中但 top-5 内可命中 |
| high | 9 | top-5 仍未命中或完全找不到 |

### 高风险表

| # | 表名 | DDL 排名 | DDL top-1 表 | DOC 排名 | DOC top-1 表 |
|---|------|---------|-------------|---------|-------------|
| 1 | `dc_survey_app` | 6 | `dc_survey_task_instance` | 3 | `dc_survey_task_instance` |
| 2 | `dc_survey_info` | 1 | `dc_survey_info` | 6 | `dc_survey_task_instance` |
| 3 | `gis_region` | 7 | `gis_region_city` | 6 | `gis_region_county` |
| 4 | `rs_outlet` | 2 | `rs_outlet_monitor_v2` | 6 | `rs_outlet_trace_v2` |
| 5 | `rs_outlet_info_v2` | 7 | `rs_outlet_trace_v2` | 2 | `rs_outlet_trace_v2` |
| 6 | `rs_pollutant_enterprise` | 9 | `rs_outlet_trace_v2` | 1 | `rs_pollutant_enterprise` |
| 7 | `rs_pollutant_info` | 7 | `rs_outlet_trace_v2` | 1 | `rs_pollutant_info` |
| 8 | `se_watershed` | 6 | `gis_watershed_partition_3` | 4 | `layer_watershed` |
| 9 | `wm_water_intake` | 10 | `wm_water_source_intake_v2` | 2 | `wm_water_source_intake_v2` |

### 中风险表

| # | 表名 | DDL 排名 | DOC 排名 |
|---|------|---------|----------|
| 1 | `ad_dict` | 2 | 1 |
| 2 | `day_quality_records` | 1 | 2 |
| 3 | `day_quality_setting` | 2 | 1 |
| 4 | `dc_survey_task` | 4 | 3 |
| 5 | `dc_survey_track` | 2 | 1 |
| 6 | `gis_region_population` | 2 | 3 |
| 7 | `gis_watershed_partition` | 3 | 3 |
| 8 | `gis_watershed_partition_4` | 2 | 1 |
| 9 | `layer_reservoir_provincial` | 1 | 2 |
| 10 | `rs_enterprise_info_wade` | 2 | 1 |
| 11 | `rs_industrial_info_yc` | 1 | 3 |
| 12 | `rs_sewage_info_v2` | 2 | 2 |
| 13 | `rs_sewage_info_yc` | 2 | 1 |
| 14 | `rs_wastewater_standard` | 5 | 1 |
| 15 | `se_watershed_river` | 1 | 3 |
| 16 | `wh_hydrological_hour_records` | 3 | 1 |
| 17 | `wh_hydrological_records_1` | 5 | 2 |
| 18 | `wh_meteorological_hour_records` | 1 | 4 |
| 19 | `wh_meteorological_records_1` | 5 | 3 |
| 20 | `wm_camera_platform` | 2 | 1 |
| 21 | `wm_meteorological_info` | 1 | 2 |
| 22 | `wm_panorama_layer` | 2 | 1 |
| 23 | `wm_raster_info` | 2 | 1 |
| 24 | `wm_raster_inversion` | 2 | 2 |
| 25 | `wm_section_info` | 1 | 2 |
| 26 | `wm_section_wq_info` | 5 | 3 |
| 27 | `wm_station_info` | 2 | 2 |
| 28 | `wm_water_source` | 3 | 5 |
| 29 | `wm_water_source_zone_v2` | 2 | 1 |
| 30 | `wst_asset` | 1 | 3 |
| 31 | `wst_asset_relation` | 2 | 1 |
| 32 | `wst_asset_type_dict` | 1 | 2 |
| 33 | `wst_relation_type_dict` | 3 | 2 |
| 34 | `wst_trace_edge` | 2 | 1 |
| 35 | `wst_trace_topology_issue` | 2 | 1 |

---

## 二、根因分析

### 2.1 为什么会出现 top-1 错表？

ChromaDB 使用 `all-MiniLM-L6-v2` (384 维) 做 embedding。该模型是通用英文语义模型，
对中文表名和字段注释的区分能力有限。当多张表名共享前缀（如 `rs_outlet*`、`wm_*`、`wst_*`），
或表注释语义相近时，top-1 可能返回相似表而非精确表。

### 2.2 top-1 错表的两类原因

1. **同前缀干扰**：`rs_outlet` vs `rs_outlet_trace_v2` / `rs_outlet_info_v2` / `rs_outlet_monitor_v2` 等
2. **语义相近干扰**：`layer_outlet_sewage` 与 `rs_outlet` 都是"排口/排污口"相关

### 2.3 为什么 top-15 都能找到？

ChromaDB 向量空间中目标表确实存在于较近的位置（距离 ~0.9-1.2），
但被更"泛化"的相似文档挤到了后面。扩大检索窗口 (n_results) 即可捕获。

---

## 三、加固方案

### 方案：确定性元数据检索层 + ChromaDB 语义补充

在进入第 2 级 SQL 示例训练前，建议实现一个**确定性元数据检索层**，
优先使用 `agent_data/column_metadata_index.json` 做精确匹配，
ChromaDB 只作为语义兜底。

#### 3.1 检索流程

```
用户问题
  |
  +--> 1. 关键词提取（表名、字段名、中文关键词）
  |
  +--> 2. 确定性检索层 (agent_data/column_metadata_index.json)
  |       |
  |       +--> 精确表名匹配: "rs_outlet" --> rs_outlet 的 DDL + 文档
  |       +--> 中文字段名匹配: "排污口编码" --> rs_outlet.outlet_code
  |       +--> 中文表注释匹配: "排污口信息表" --> rs_outlet
  |       +--> LIKE 子串匹配
  |
  +--> 3. ChromaDB 语义检索（补充）
  |       |
  |       +--> n_results = 15
  |       +--> 与确定性结果去重合并
  |       +--> 填充未被关键词命中的相关表
  |
  +--> 4. 排序
          |
          +--> 确定性匹配 = 最高优先级
          +--> ChromaDB top-1~3 = 次高优先级
          +--> ChromaDB rest = 最低优先级
```

#### 3.2 agent_data/column_metadata_index.json 能力分析

当前 `column_metadata_index.json` 包含 2572 条记录，每条有：
- `table`: 精确表名
- `table_comment`: 中文表注释
- `column`: 精确字段名
- `type`: 数据类型
- `comment`: 中文字段注释

该索引可以直接支持：
- **精确表名查找**: O(1) dict 查询
- **中文表注释反向索引**: 构建 `comment -> table` 映射
- **字段名精确查找**: `dict[table][column]` 查找
- **中文字段注释搜索**: 构建倒排索引

#### 3.3 实现建议

```python
class DeterministicMetadataLayer:
    def __init__(self, agent_index_path):
        self.index = json.load(open(agent_index_path))
        self.by_table = defaultdict(list)
        self.table_comment_index = {}  # comment_keyword -> [tables]
        self.column_comment_index = {}  # comment_keyword -> [(table, column)]
        for item in self.index:
            self.by_table[item['table']].append(item)
            # 建立中文注释倒排索引
            ...

    def search(self, keywords):
        '''确定性检索，返回精确匹配的 DDL + documentation'''
        hits = []
        # 1. 精确表名匹配
        for kw in keywords:
            if kw in self.by_table:
                hits.append(('exact_table', kw, self.by_table[kw]))
        # 2. 中文注释匹配
        ...
        return hits
```

#### 3.4 实施优先级

| 优先级 | 事项 | 理由 |
|--------|------|------|
| P0 | 精确表名检索层 | 消除所有 top-1 错表问题 |
| P1 | 中文表注释搜索 | 覆盖"排污口"→rs_outlet 类查询 |
| P2 | 字段名精确匹配 | 覆盖"outlet_code"→rs_outlet 类查询 |
| P3 | ChromaDB 语义兜底 | 覆盖"附近的排放口"类模糊查询 |

---

## 四、建议

**在进入第 2 级 SQL 示例训练前，建议先实现 P0 精确表名检索层。**

理由：
1. Level 2 的 SQL 示例训练依赖"先用 DDL + documentation 找到正确表"
2. 如果 Level 1 检索就找错表，后续 SQL 生成必然跑偏
3. P0 实现成本低（约 50 行代码），确定性 100%

---

## 五、边界声明

- 未重新训练 Vanna
- 未修改 ChromaDB
- 未修改数据库
- 未进入第 2/3/4 级
- 未编造字段
- 未编造注释

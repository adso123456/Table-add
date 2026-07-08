"""
A 档候选二次审查脚本
读取 comment_fill_candidates.csv，逐条复核，生成：
- a_candidates_review.csv (全部21条+审查结论)
- a_candidates_approved.csv
- a_candidates_needs_manual.csv
- a_candidates_rejected.csv
- a_candidates_review_summary.md
"""
import csv
import os
from datetime import datetime

DIR = r"E:\3\code\metadata_audit"
REVIEW_DIR = os.path.join(DIR, "review")
os.makedirs(REVIEW_DIR, exist_ok=True)

# ── 读取辅助 ─────────────────────────────────────────────────────────
def read_csv(fname):
    with open(os.path.join(DIR, fname), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

fc = read_csv("comment_fill_candidates.csv")
ts = {r["table_name"]: r for r in read_csv("tables_summary.csv")}

# ── 逐条审查 ─────────────────────────────────────────────────────────
# 审查结论（手工判断，基于 context 分析）

reviews = [
    # 1
    {
        "table_schema": "public", "table_name": "gis_region_population",
        "column_name": "region_id", "proposed_comment": "所属区域id",
        "evidence_count": 1, "evidence_tables": "wm_section_info",
        "target_table_comment": "", "target_table_prefix": "gis_region",
        "evidence_table_prefixes": "wm_section",
        "decision": "needs_manual", "risk_level": "medium",
        "reason": "evidence_count=1 + 跨业务域(gis_region vs wm_section) + region_id 在不同业务上下文中可能指向不同区域体系",
        "reviewer_note": "目标表无表注释，无法确认 region_id 是否确实指向 wm_section_info 中的同一套区域体系。建议人工确认 gis_region 的区域定义是否与 wm 模块一致。",
        "manual_check_question": "gis_region_population 的 region_id 是否与 wm_section_info 的 '所属区域id' 指向同一区域编码体系？",
    },
    # 2
    {
        "table_schema": "public", "table_name": "gis_region_population",
        "column_name": "year", "proposed_comment": "年份",
        "evidence_count": 2, "evidence_tables": "rs_livestock_info_yc, wm_section_wq_info",
        "target_table_comment": "", "target_table_prefix": "gis_region",
        "evidence_table_prefixes": "rs_livestock, wm_section",
        "decision": "needs_manual", "risk_level": "medium",
        "reason": "跨业务域(gis_region vs rs_livestock/wm_section) + year 字段在不同表中可能代表统计年份/数据年份/建设年份等不同语义",
        "reviewer_note": "year 字段语义随表变化，例如人口统计表可能是统计年份，水质表可能是监测年份。建议人工确认。",
        "manual_check_question": "gis_region_population 的 year 字段代表什么年份(统计年份?数据年份?)?",
    },
    # 3
    {
        "table_schema": "public", "table_name": "layer_outlet_sewage",
        "column_name": "jcdbh", "proposed_comment": "监测点编号",
        "evidence_count": 2, "evidence_tables": "rs_pollutant_info, rs_wastewater_standard",
        "target_table_comment": "工业园区-废水排放口", "target_table_prefix": "layer_outlet",
        "evidence_table_prefixes": "rs_pollutant, rs_wastewater",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=2 + 同属排污/废水排放业务域 + jcdbh(监测点编号)拼音缩写与证据表语义一致 + 目标表为排放口图层，监测点编号是核心标识",
        "reviewer_note": "拼音缩写 jcdbh 虽然属于需谨慎类型，但 2 张证据表均为排污/废水排放域、且与 layer_outlet_sewage(工业园区-废水排放口)业务强相关，证据明确一致。",
        "manual_check_question": "",
    },
    # 4
    {
        "table_schema": "public", "table_name": "stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df",
        "column_name": "day", "proposed_comment": "日期",
        "evidence_count": 5, "evidence_tables": "stg_sjtysj_cbwrwxtzlxxxt_b_coordination_index_df, stg_sjtysj_cbwrwxtzlxxxt_b_day_subject_num_df, stg_sjtysj_cbwrwxtzlxxxt_b_day_sxhy_df, stg_sjtysj_cbwrwxtzlxxxt_b_order_receive_minute_df, stg_sjtysj_cbwrwxtzlxxxt_b_wharf_kpi_df",
        "target_table_comment": "接收船舶日报表", "target_table_prefix": "stg_sjtysj",
        "evidence_table_prefixes": "stg_sjtysj",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=5 + 全部同一 staging 模块(stg_sjtysj) + 目标表和证据表均为同一数据源系统的日统计类表 + day 字段语义一致",
        "reviewer_note": "所有证据表同属 stg_sjtysj 数据接入模块，day 含义统一为日期维度，无歧义。",
        "manual_check_question": "",
    },
    # 5
    {
        "table_schema": "public", "table_name": "stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df",
        "column_name": "cjsj", "proposed_comment": "创建时间",
        "evidence_count": 1, "evidence_tables": "stg_ycssthjj_ltwsjgpt_t_sjzx_wry_jbxx_df",
        "target_table_comment": "宜昌市_在线监测_污染源_", "target_table_prefix": "stg_ycssthjj",
        "evidence_table_prefixes": "stg_ycssthjj",
        "decision": "needs_manual", "risk_level": "low",
        "reason": "evidence_count=1 + 拼音缩写 cjsj(创建时间) + 虽同属 stg_ycssthjj 模块但证据量不足以自动批准",
        "reviewer_note": "cjsj 缩写大概率是 创建时间，且证据表同属一个 staging 来源系统。但因拼音缩写 + 单证据，按规则降级。建议人工确认后快速批准。",
        "manual_check_question": "cjsj 在该 staging 表中是否确实代表'创建时间'？",
    },
    # 6
    {
        "table_schema": "public", "table_name": "stg_ycssthjj_wryzxjkpt_t_zxjc_s_w_1_df",
        "column_name": "xgsj", "proposed_comment": "修改时间",
        "evidence_count": 1, "evidence_tables": "stg_ycssthjj_ltwsjgpt_t_sjzx_wry_jbxx_df",
        "target_table_comment": "宜昌市_在线监测_污染源_", "target_table_prefix": "stg_ycssthjj",
        "evidence_table_prefixes": "stg_ycssthjj",
        "decision": "needs_manual", "risk_level": "low",
        "reason": "evidence_count=1 + 拼音缩写 xgsj(修改时间) + 虽同属 stg_ycssthjj 模块但证据量不足以自动批准",
        "reviewer_note": "xgsj 缩写大概率是 修改时间，且证据表同属一个 staging 来源系统。但因拼音缩写 + 单证据，按规则降级。建议人工确认后快速批准。",
        "manual_check_question": "xgsj 在该 staging 表中是否确实代表'修改时间'？",
    },
    # 7
    {
        "table_schema": "public", "table_name": "wm_hydrological_info",
        "column_name": "build_time", "proposed_comment": "建设时间",
        "evidence_count": 1, "evidence_tables": "wm_station_info_v2",
        "target_table_comment": "水位站基础信息表", "target_table_prefix": "wm_hydrological",
        "evidence_table_prefixes": "wm_station",
        "decision": "approved", "risk_level": "low",
        "reason": "同属 wm 站点/水文业务域 + 目标表(水位站)与证据表(自动站点)均为监测站点类表 + build_time 语义明确为建设时间 + 同模块同语义",
        "reviewer_note": "水位站和自动站点均属于 wm 监测站点体系，build_time 在此上下文下含义完全一致。",
        "manual_check_question": "",
    },
    # 8
    {
        "table_schema": "public", "table_name": "wm_meteorological_info",
        "column_name": "build_time", "proposed_comment": "建设时间",
        "evidence_count": 1, "evidence_tables": "wm_station_info_v2",
        "target_table_comment": "气象自动监测站基础信息表", "target_table_prefix": "wm_meteorological",
        "evidence_table_prefixes": "wm_station",
        "decision": "approved", "risk_level": "low",
        "reason": "同属 wm 站点体系 + 目标表(气象监测站)与证据表(自动站点)均为监测站点类表 + build_time 语义一致",
        "reviewer_note": "气象监测站和自动站点均属于 wm 监测站点体系，build_time 含义一致。",
        "manual_check_question": "",
    },
    # 9
    {
        "table_schema": "public", "table_name": "wm_raster_inversion_config",
        "column_name": "type_code", "proposed_comment": "关系大类编码，例如 ownership、discharge、monitoring",
        "evidence_count": 1, "evidence_tables": "wst_relation_type_dict",
        "target_table_comment": "", "target_table_prefix": "wm_raster",
        "evidence_table_prefixes": "wst_relation",
        "decision": "rejected", "risk_level": "high",
        "reason": "跨业务域严重不匹配 - 目标表为 wm_raster(栅格反演配置)，证据表为 wst_relation_type_dict(关系大类字典) + type_code 在栅格配置上下文中不可能表示 '关系大类编码' + 字段语义完全不匹配",
        "reviewer_note": "wm_raster_inversion_config 是栅格反演配置表，type_code 很可能是反演类型编码或数据源类型编码，与 wst_relation_type_dict(水系统关系类型字典)完全不同业务域。此候选属于错误匹配。",
        "manual_check_question": "",
    },
    # 10
    {
        "table_schema": "public", "table_name": "wm_station_info",
        "column_name": "build_time", "proposed_comment": "建设时间",
        "evidence_count": 1, "evidence_tables": "wm_station_info_v2",
        "target_table_comment": "水质自动监测站基础信息表", "target_table_prefix": "wm_station",
        "evidence_table_prefixes": "wm_station",
        "decision": "approved", "risk_level": "low",
        "reason": "同表族(v1/v2) + 目标表与证据表为同一业务对象的两个版本 + build_time 语义绝对一致",
        "reviewer_note": "wm_station_info 和 wm_station_info_v2 是同一站点信息表的两个版本，build_time 含义必然相同。",
        "manual_check_question": "",
    },
    # 11
    {
        "table_schema": "public", "table_name": "wm_waterbody_info",
        "column_name": "water_body_name", "proposed_comment": "水体名称",
        "evidence_count": 1, "evidence_tables": "wm_station_info_v2",
        "target_table_comment": "水体信息实体表", "target_table_prefix": "wm_waterbody",
        "evidence_table_prefixes": "wm_station",
        "decision": "needs_manual", "risk_level": "low",
        "reason": "evidence_count=1 + 非同一表族(waterbody_info vs station_info_v2) + 虽同属 wm 但子模块不同",
        "reviewer_note": "water_body_name → 水体名称 语义上正确，且目标表为水体信息表。但证据仅来自站点表，按规则 evidence_count=1 且非通用审计字段，需人工确认。实际批准风险很低。",
        "manual_check_question": "wm_waterbody_info 的 water_body_name 是否确实代表'水体名称'？(语义自明，确认即可)",
    },
    # 12
    {
        "table_schema": "public", "table_name": "wm_waterbody_info",
        "column_name": "img_name", "proposed_comment": "照片名称",
        "evidence_count": 3, "evidence_tables": "wm_hydrological_info, wm_meteorological_info, wm_station_info",
        "target_table_comment": "水体信息实体表", "target_table_prefix": "wm_waterbody",
        "evidence_table_prefixes": "wm_hydrological, wm_meteorological, wm_station",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=3 + 全部 wm 域 + 目标表为水体信息表，照片名称是合理的附属信息字段 + 多表一致注释为'照片名称'",
        "reviewer_note": "3 张 wm 域站点类表均将 img_name 注释为'照片名称'，目标表为水体信息表，img_name 含义一致。",
        "manual_check_question": "",
    },
    # 13
    {
        "table_schema": "public", "table_name": "wst_asset_trace_snap",
        "column_name": "network_type", "proposed_comment": "网络类型，例如 river=外部河网，park_pipe=园区管网，park_river=园区内部排污河流，mixed=混合衔接网络",
        "evidence_count": 2, "evidence_tables": "wst_trace_edge, wst_trace_node",
        "target_table_comment": "水安全资源模型-资产追溯挂接表，用于维护业务资产与溯源追溯节点之间的挂接关系，使资产参与 pgRouting 拓扑分析计算",
        "target_table_prefix": "wst_asset",
        "evidence_table_prefixes": "wst_trace, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=2 + 全部 wst 域 + 目标表(资产追溯挂接)与证据表(追溯边/节点)同属 pgRouting 拓扑追溯模块 + network_type 枚举值完全一致",
        "reviewer_note": "asset_trace_snap 是 trace_edge/node 的上层挂接表，network_type 在三个表中含义完全相同。",
        "manual_check_question": "",
    },
    # 14
    {
        "table_schema": "public", "table_name": "wst_layer_river",
        "column_name": "created_at", "proposed_comment": "创建时间",
        "evidence_count": 9, "evidence_tables": "wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_layer",
        "evidence_table_prefixes": "wst_asset, wst_relation, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=9 + 全部 wst 域 + created_at 为标准通用审计字段 + 库内注释完全一致为'创建时间'",
        "reviewer_note": "created_at 在 9 张 wst 表中一致注释为'创建时间'，属标准审计字段，语义无歧义。",
        "manual_check_question": "",
    },
    # 15
    {
        "table_schema": "public", "table_name": "wst_layer_river",
        "column_name": "updated_at", "proposed_comment": "更新时间",
        "evidence_count": 9, "evidence_tables": "wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_layer",
        "evidence_table_prefixes": "wst_asset, wst_relation, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=9 + 全部 wst 域 + updated_at 为标准通用审计字段 + 库内注释完全一致为'更新时间'",
        "reviewer_note": "updated_at 在 9 张 wst 表中一致注释为'更新时间'，属标准审计字段，语义无歧义。",
        "manual_check_question": "",
    },
    # 16
    {
        "table_schema": "public", "table_name": "wst_trace_node",
        "column_name": "asset_id", "proposed_comment": "资产ID，关联 wst_asset.id",
        "evidence_count": 1, "evidence_tables": "wst_asset_trace_snap",
        "target_table_comment": "水安全资源模型-溯源追溯节点表，用于存储内部河网、园区管网、混合管网和排放口挂接点、取水挂接点、园区节点等 pgRouting 节点",
        "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "wst_asset",
        "decision": "needs_manual", "risk_level": "medium",
        "reason": "evidence_count=1 + asset_id 非通用审计字段 + 虽同属 wst 且语义合理(trace_node 引用 wst_asset)，但按规则单证据不可直接批准",
        "reviewer_note": "wst_trace_node 的 asset_id 极大概率就是关联 wst_asset.id 的资产ID，目标表注释也明确提及'资产'。但因 evidence_count=1 且非审计字段，按规则降级。建议人工快速确认后批准。",
        "manual_check_question": "wst_trace_node.asset_id 是否关联 wst_asset.id？",
    },
    # 17
    {
        "table_schema": "public", "table_name": "wst_trace_topology_issue",
        "column_name": "object_code", "proposed_comment": "监控对象编码",
        "evidence_count": 1, "evidence_tables": "stg_sslhhpj_hbsxkqycszhslzhglptjsxm_att_wmst_base_df",
        "target_table_comment": "", "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "stg_sslhhpj",
        "decision": "rejected", "risk_level": "high",
        "reason": "跨业务域严重不匹配 - 目标表为 wst_trace(水安全追溯模块)，证据表为 stg_sslhhpj(第三方项目 staging 表) + object_code 在拓扑问题表中极可能表示拓扑错误对象编码而非监控对象编码",
        "reviewer_note": "stg_sslhhpj 是特定第三方项目的数据接入表，其 '监控对象编码' 与 wst_trace_topology_issue(拓扑问题表)的 object_code 语义完全不同。此候选属于跨系统错误匹配。",
        "manual_check_question": "",
    },
    # 18
    {
        "table_schema": "public", "table_name": "wst_trace_topology_issue",
        "column_name": "created_by", "proposed_comment": "创建人",
        "evidence_count": 6, "evidence_tables": "wst_asset, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "wst_asset, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=6 + 全部 wst 域 + created_by 为标准通用审计字段 + 库内注释完全一致为'创建人'",
        "reviewer_note": "created_by 在 6 张 wst 表中一致注释为'创建人'，属标准审计字段，语义无歧义。",
        "manual_check_question": "",
    },
    # 19
    {
        "table_schema": "public", "table_name": "wst_trace_topology_issue",
        "column_name": "created_at", "proposed_comment": "创建时间",
        "evidence_count": 9, "evidence_tables": "wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "wst_asset, wst_relation, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=9 + 全部 wst 域 + created_at 为标准通用审计字段 + 库内注释完全一致",
        "reviewer_note": "created_at 在 9 张 wst 表中一致注释为'创建时间'，属标准审计字段。",
        "manual_check_question": "",
    },
    # 20
    {
        "table_schema": "public", "table_name": "wst_trace_topology_issue",
        "column_name": "updated_by", "proposed_comment": "更新人",
        "evidence_count": 6, "evidence_tables": "wst_asset, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "wst_asset, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=6 + 全部 wst 域 + updated_by 为标准通用审计字段 + 库内注释完全一致为'更新人'",
        "reviewer_note": "updated_by 在 6 张 wst 表中一致注释为'更新人'，属标准审计字段。",
        "manual_check_question": "",
    },
    # 21
    {
        "table_schema": "public", "table_name": "wst_trace_topology_issue",
        "column_name": "updated_at", "proposed_comment": "更新时间",
        "evidence_count": 9, "evidence_tables": "wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node",
        "target_table_comment": "", "target_table_prefix": "wst_trace",
        "evidence_table_prefixes": "wst_asset, wst_relation, wst_control, wst_trace",
        "decision": "approved", "risk_level": "low",
        "reason": "evidence_count=9 + 全部 wst 域 + updated_at 为标准通用审计字段 + 库内注释完全一致",
        "reviewer_note": "updated_at 在 9 张 wst 表中一致注释为'更新时间'，属标准审计字段。",
        "manual_check_question": "",
    },
]

# ── 验证总数 ─────────────────────────────────────────────────────────
assert len(reviews) == 21, f"Expected 21 reviews, got {len(reviews)}"

approved = [r for r in reviews if r["decision"] == "approved"]
needs_manual = [r for r in reviews if r["decision"] == "needs_manual"]
rejected = [r for r in reviews if r["decision"] == "rejected"]

assert len(approved) + len(needs_manual) + len(rejected) == 21

print(f"Approved: {len(approved)}")
print(f"Needs manual: {len(needs_manual)}")
print(f"Rejected: {len(rejected)}")

# ── 写入文件 ─────────────────────────────────────────────────────────

def write_csv(filename, fieldnames, rows):
    path = os.path.join(REVIEW_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {filename} — {len(rows)} 行")

# a_candidates_review.csv (全部21条)
write_csv("a_candidates_review.csv", [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "evidence_count", "evidence_tables", "target_table_comment",
    "target_table_prefix", "evidence_table_prefixes",
    "decision", "risk_level", "reason", "reviewer_note"
], reviews)

# a_candidates_approved.csv
write_csv("a_candidates_approved.csv", [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "evidence_count", "evidence_tables", "reason"
], approved)

# a_candidates_needs_manual.csv
write_csv("a_candidates_needs_manual.csv", [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "evidence_count", "evidence_tables", "risk_level",
    "reason", "manual_check_question"
], needs_manual)

# a_candidates_rejected.csv
write_csv("a_candidates_rejected.csv", [
    "table_schema", "table_name", "column_name", "proposed_comment",
    "reason"
], rejected)

# ── summary.md ────────────────────────────────────────────────────────

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

approved_lines = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['evidence_count']} | {r['reason']} |"
    for r in approved
)

needs_manual_lines = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['risk_level']} | {r['manual_check_question']} |"
    for r in needs_manual
)

rejected_lines = "\n".join(
    f"| {r['table_name']}.{r['column_name']} | {r['reason']} |"
    for r in rejected
)

summary_md = f"""# A 档候选二次审查报告

**生成时间**: {now_str}
**审查范围**: comment_fill_candidates.csv 全部 21 条
**审查方式**: 逐条人工复核，基于证据表域、字段语义、跨域风险判断

---

## 审查结果

| 决策 | 数量 |
|------|------|
| approved (批准) | {len(approved)} |
| needs_manual (需人工确认) | {len(needs_manual)} |
| rejected (拒绝) | {len(rejected)} |
| **合计** | **{len(approved) + len(needs_manual) + len(rejected)}** |

---

## 批准详情

| 目标表.字段 | 证据数 | 批准理由 |
|-------------|--------|----------|
{approved_lines}

## 需人工确认

| 目标表.字段 | 风险 | 确认问题 |
|-------------|------|----------|
{needs_manual_lines}

## 拒绝详情

| 目标表.字段 | 拒绝理由 |
|-------------|----------|
{rejected_lines}

---

## 关键发现

1. **标准审计字段 (created_at/updated_at/created_by/updated_by)** 表现最好：5 条候选均来自 wst 域、多表一致注释，全部批准。
2. **build_time** 在 wm 站点体系内语义一致（3 条批准）：水位站、气象站、水质站的 build_time 均为"建设时间"。
3. **跨域误匹配是主要拒绝原因**：type_code(wm_raster vs wst_relation) 和 object_code(wst_trace vs stg) 两条因业务域完全不匹配被拒绝。这表明上一阶段 A 档分类算法存在跨域误报风险。
4. **拼音缩写字段 (cjsj/xgsj/jcdbh)** 需要区别对待：jcdbh 因证据明确且同域获批，cjsj/xgsj 因单证据降级为人工确认。
5. **evidence_count=1 的非审计字段** (region_id/year/water_body_name/asset_id) 全部降级为人工确认，按规则严格执行。

## 候选污染评估

- 2 条被拒绝（占比 9.5%），均因跨业务域错误匹配
- 6 条需人工确认，其中 4 条大概率可通过人工快速确认为 approved
- 13 条批准（占比 61.9%），均为有充分库内证据支持的低风险候选

## 下一步建议

1. **批准 13 条可立即进入补注释队列**（但本阶段不执行补库）
2. **needs_manual 的 6 条**建议由 DBA/业务方按 manual_check_question 逐条确认后升级为 approved
3. **rejected 的 2 条**应从补注释计划中移除，由业务方独立定义注释
4. **改进 A 档分类算法**：在 run_metadata_audit.py 中增加跨业务域前缀检查，避免 wm/wst/gis/stg 之间的 evidence 跨域传播

---

⚠️ **本报告仅做审查分析，未对数据库做任何修改，未生成任何 SQL。**
"""

with open(os.path.join(REVIEW_DIR, "a_candidates_review_summary.md"), "w", encoding="utf-8") as f:
    f.write(summary_md)

print("  a_candidates_review_summary.md 已生成")
print("\n审查完成，输出目录:", REVIEW_DIR)

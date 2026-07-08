-- ============================================================================
-- DRAFT ONLY — COMMENT ON COLUMN SQL 草案
-- ============================================================================
-- 本文件仅为人工审查草案，尚未执行。
-- 来源：a_candidates_approved.csv (13 条) + a_candidates_verify_report.csv (全部 pass)
-- 生成时间：2026-07-07 15:40:22
--
-- ⚠️  禁止未经人工确认直接在生产库执行。
-- ⚠️  执行前请逐条核对注释内容与业务含义是否匹配。
-- ============================================================================
-- #1: layer_outlet_sewage.jcdbh
-- Evidence: 2 table(s) — rs_pollutant_info, rs_wastewater_standard
COMMENT ON COLUMN public."layer_outlet_sewage"."jcdbh" IS '监测点编号';

-- #2: stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df.day
-- Evidence: 5 table(s) — stg_sjtysj_cbwrwxtzlxxxt_b_coordination_index_df, stg_sjtysj_cbwrwxtzlxxxt_b_day_subject_num_df, stg_sjtysj_cbwrwxtzlxxxt_b_day_sxhy_df, stg_sjtysj_cbwrwxtzlxxxt_b_order_receive_minute_df, stg_sjtysj_cbwrwxtzlxxxt_b_wharf_kpi_df
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df"."day" IS '日期';

-- #3: wm_hydrological_info.build_time
-- Evidence: 1 table(s) — wm_station_info_v2
COMMENT ON COLUMN public."wm_hydrological_info"."build_time" IS '建设时间';

-- #4: wm_meteorological_info.build_time
-- Evidence: 1 table(s) — wm_station_info_v2
COMMENT ON COLUMN public."wm_meteorological_info"."build_time" IS '建设时间';

-- #5: wm_station_info.build_time
-- Evidence: 1 table(s) — wm_station_info_v2
COMMENT ON COLUMN public."wm_station_info"."build_time" IS '建设时间';

-- #6: wm_waterbody_info.img_name
-- Evidence: 3 table(s) — wm_hydrological_info, wm_meteorological_info, wm_station_info
COMMENT ON COLUMN public."wm_waterbody_info"."img_name" IS '照片名称';

-- #7: wst_asset_trace_snap.network_type
-- Evidence: 2 table(s) — wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_asset_trace_snap"."network_type" IS '网络类型，例如 river=外部河网，park_pipe=园区管网，park_river=园区内部排污河流，mixed=混合衔接网络';

-- #8: wst_layer_river.created_at
-- Evidence: 9 table(s) — wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_layer_river"."created_at" IS '创建时间';

-- #9: wst_layer_river.updated_at
-- Evidence: 9 table(s) — wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_layer_river"."updated_at" IS '更新时间';

-- #10: wst_trace_topology_issue.created_by
-- Evidence: 6 table(s) — wst_asset, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_trace_topology_issue"."created_by" IS '创建人';

-- #11: wst_trace_topology_issue.created_at
-- Evidence: 9 table(s) — wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_trace_topology_issue"."created_at" IS '创建时间';

-- #12: wst_trace_topology_issue.updated_by
-- Evidence: 6 table(s) — wst_asset, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_trace_topology_issue"."updated_by" IS '更新人';

-- #13: wst_trace_topology_issue.updated_at
-- Evidence: 9 table(s) — wst_asset, wst_asset_relation, wst_asset_trace_snap, wst_asset_type_dict, wst_control_zone, wst_relation_subtype_dict, wst_relation_type_dict, wst_trace_edge, wst_trace_node
COMMENT ON COLUMN public."wst_trace_topology_issue"."updated_at" IS '更新时间';


-- ==========================================
-- B_review approved 注释批量 SQL 草案
-- 生成时间: 2026-07-08 14:31:10
-- 状态: 草案，待人工执行前最终确认，未执行
-- 字段: 212 条 (全部 human_decision=approve)
-- 警告: 执行前需人工检查对象存在性
-- ==========================================

-- _stg_yichang_river_import
COMMENT ON COLUMN public."_stg_yichang_river_import"."Nextdown" IS '下游河流ID';
COMMENT ON COLUMN public."_stg_yichang_river_import"."MAINRIVID" IS '干流ID';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Hydrocount" IS '水文计数';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Rclass" IS '河流类别编码';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Rlenth" IS '河流长度';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Hydrolenth" IS '水文计算长度';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Rcatch" IS '汇水面积';
COMMENT ON COLUMN public."_stg_yichang_river_import"."TCatch" IS '总汇水面积';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Rname" IS '河流名称';
COMMENT ON COLUMN public."_stg_yichang_river_import"."Shape_Leng" IS '要素长度';
COMMENT ON COLUMN public."_stg_yichang_river_import"."RiverID" IS '河流ID';
COMMENT ON COLUMN public."_stg_yichang_river_import"."NameList" IS '河流名称列表';
COMMENT ON COLUMN public."_stg_yichang_river_import"."SEG_ID" IS '分段ID';
COMMENT ON COLUMN public."_stg_yichang_river_import"."LEN" IS '分段长度';
COMMENT ON COLUMN public."_stg_yichang_river_import"."FROM_Z" IS '起点高程';
COMMENT ON COLUMN public."_stg_yichang_river_import"."TO_Z" IS '终点高程';
COMMENT ON COLUMN public."_stg_yichang_river_import"."STR_ORD" IS 'Strahler河流分级';
COMMENT ON COLUMN public."_stg_yichang_river_import"."SHR_ORD" IS 'Shreve河流分级';

-- _stg_yichang_river_std
COMMENT ON COLUMN public."_stg_yichang_river_std"."next_down" IS '下游河流ID';
COMMENT ON COLUMN public."_stg_yichang_river_std"."river_class" IS '河流类别';
COMMENT ON COLUMN public."_stg_yichang_river_std"."length_km" IS '河流长度（公里）';
COMMENT ON COLUMN public."_stg_yichang_river_std"."from_z" IS '起点高程';
COMMENT ON COLUMN public."_stg_yichang_river_std"."to_z" IS '终点高程';

-- gis_ecologicalregion
COMMENT ON COLUMN public."gis_ecologicalregion"."service_target" IS '生态服务目标';
COMMENT ON COLUMN public."gis_ecologicalregion"."ecosystem_vegetation" IS '生态系统植被概况';
COMMENT ON COLUMN public."gis_ecologicalregion"."human_activities" IS '人类活动影响描述';
COMMENT ON COLUMN public."gis_ecologicalregion"."environment_problems" IS '生态环境问题描述';
COMMENT ON COLUMN public."gis_ecologicalregion"."control_measures" IS '管控措施描述';

-- gis_headwaters
COMMENT ON COLUMN public."gis_headwaters"."water_intake_quantity" IS '年取水量';
COMMENT ON COLUMN public."gis_headwaters"."water_supply_population" IS '供水人口数';
COMMENT ON COLUMN public."gis_headwaters"."is_protect_region" IS '是否在保护区范围内';

-- gis_naturereserve
COMMENT ON COLUMN public."gis_naturereserve"."department" IS '主管部门';
COMMENT ON COLUMN public."gis_naturereserve"."protect_target" IS '主要保护对象';
COMMENT ON COLUMN public."gis_naturereserve"."manage_org_name" IS '管理机构名称';
COMMENT ON COLUMN public."gis_naturereserve"."manage_org_type" IS '管理机构类型';
COMMENT ON COLUMN public."gis_naturereserve"."manage_org_level" IS '管理机构级别';
COMMENT ON COLUMN public."gis_naturereserve"."first_protect_animals" IS '国家一级保护动物';
COMMENT ON COLUMN public."gis_naturereserve"."second_protect_animals" IS '国家二级保护动物';
COMMENT ON COLUMN public."gis_naturereserve"."first_protect_plants" IS '国家一级保护植物';
COMMENT ON COLUMN public."gis_naturereserve"."second_protect_plants" IS '国家二级保护植物';

-- gis_region
COMMENT ON COLUMN public."gis_region"."region_level" IS '区划级别';
COMMENT ON COLUMN public."gis_region"."parent_code" IS '父级区划编码';

-- gis_region_population
COMMENT ON COLUMN public."gis_region_population"."city_population" IS '城镇人口';
COMMENT ON COLUMN public."gis_region_population"."city_area" IS '城镇面积';
COMMENT ON COLUMN public."gis_region_population"."city_quantity" IS '城镇数量';
COMMENT ON COLUMN public."gis_region_population"."rural_population" IS '农村人口';
COMMENT ON COLUMN public."gis_region_population"."rural_area" IS '农村面积';
COMMENT ON COLUMN public."gis_region_population"."rural_quantity" IS '农村数量';

-- gis_watershed_partition_4
COMMENT ON COLUMN public."gis_watershed_partition_4"."poly_area" IS '多边形面积';

-- layer_reservoir_provincial
COMMENT ON COLUMN public."layer_reservoir_provincial"."cc" IS '行政区划编码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."gb" IS '国标编码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."bas" IS '流域编码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."period" IS '时期/阶段';
COMMENT ON COLUMN public."layer_reservoir_provincial"."wq" IS '水质类别';
COMMENT ON COLUMN public."layer_reservoir_provincial"."aheight" IS '坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial"."parea" IS '永久占地面积';
COMMENT ON COLUMN public."layer_reservoir_provincial"."ec" IS '生态分区编码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."grade" IS '等级/级别';
COMMENT ON COLUMN public."layer_reservoir_provincial"."mheight" IS '最大坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial"."sdtf" IS '水系特征码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."shrc" IS '所属河湖编码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."vol" IS '库容';
COMMENT ON COLUMN public."layer_reservoir_provincial"."featid" IS '要素唯一标识';
COMMENT ON COLUMN public."layer_reservoir_provincial"."areacode" IS '行政区划代码';
COMMENT ON COLUMN public."layer_reservoir_provincial"."changetype" IS '变更类型';
COMMENT ON COLUMN public."layer_reservoir_provincial"."shape_leng" IS '要素长度';
COMMENT ON COLUMN public."layer_reservoir_provincial"."shape_area" IS '要素面积';

-- layer_reservoir_provincial_label
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."cc" IS '行政区划编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."gb" IS '国标编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."bas" IS '流域编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."period" IS '时期/阶段';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."wq" IS '水质类别';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."aheight" IS '坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."parea" IS '永久占地面积';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."ec" IS '生态分区编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."grade" IS '等级/级别';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."mheight" IS '最大坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."sdtf" IS '水系特征码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."shrc" IS '所属河湖编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."vol" IS '库容';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."featid" IS '要素唯一标识';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."areacode" IS '行政区划代码';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."changetype" IS '变更类型';

-- layer_reservoir_provincial_合并
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."cc" IS '行政区划编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."gb" IS '国标编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."bas" IS '流域编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."period" IS '时期/阶段';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."wq" IS '水质类别';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."aheight" IS '坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."parea" IS '永久占地面积';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."ec" IS '生态分区编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."grade" IS '等级/级别';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."mheight" IS '最大坝高';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."sdtf" IS '水系特征码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."shrc" IS '所属河湖编码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."vol" IS '库容';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."featid" IS '要素唯一标识';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."areacode" IS '行政区划代码';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."changetype" IS '变更类型';

-- layer_river_provincial
COMMENT ON COLUMN public."layer_river_provincial"."cc" IS '行政区划编码';
COMMENT ON COLUMN public."layer_river_provincial"."gb" IS '国标编码';
COMMENT ON COLUMN public."layer_river_provincial"."bas" IS '流域编码';
COMMENT ON COLUMN public."layer_river_provincial"."ec" IS '生态分区编码';
COMMENT ON COLUMN public."layer_river_provincial"."grade" IS '等级/级别';
COMMENT ON COLUMN public."layer_river_provincial"."period" IS '时期/阶段';
COMMENT ON COLUMN public."layer_river_provincial"."shrc" IS '所属河湖编码';
COMMENT ON COLUMN public."layer_river_provincial"."sdtf" IS '水系特征码';
COMMENT ON COLUMN public."layer_river_provincial"."featid" IS '要素唯一标识';
COMMENT ON COLUMN public."layer_river_provincial"."areacode" IS '行政区划代码';
COMMENT ON COLUMN public."layer_river_provincial"."changetype" IS '变更类型';

-- layer_river_provincial_bak0617
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."cc" IS '行政区划编码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."gb" IS '国标编码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."bas" IS '流域编码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."ec" IS '生态分区编码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."grade" IS '等级/级别';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."period" IS '时期/阶段';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."shrc" IS '所属河湖编码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."sdtf" IS '水系特征码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."featid" IS '要素唯一标识';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."areacode" IS '行政区划代码';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."changetype" IS '变更类型';

-- metadata_view
COMMENT ON COLUMN public."metadata_view"."aliasname" IS '别名';
COMMENT ON COLUMN public."metadata_view"."LayerName" IS '图层名称';
COMMENT ON COLUMN public."metadata_view"."LayerType" IS '图层类型';

-- wh_meteorological_predict_day_records
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."winddirect_10m_24h" IS '10米风向（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."winddirect8_10m_24h" IS '10米8方位风向（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."winddirect16_10m_24h" IS '10米16方位风向（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."hum_2m_24h" IS '2米湿度（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."hum_2m_24h_min" IS '2米湿度最小值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."hum_2m_24h_max" IS '2米湿度最大值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."stapress_24h" IS '地面气压（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."pressure_24h" IS '海平面气压（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."p850inver_24h" IS '850hPa逆温层高度（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."p925inver_24h" IS '925hPa逆温层高度（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."swdown_24h" IS '短波辐射通量（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."glw_24h" IS '长波辐射通量（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."height_24h" IS '边界层高度（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."rain_24h_total" IS '24小时总降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."dewpoint_24h" IS '露点温度（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."lowcloud_24h" IS '低云量（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."midcloud_24h" IS '中云量（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."highcloud_24h" IS '高云量（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."totalcloud_24h" IS '总云量（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."tem_2m_24h" IS '2米温度（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."tem_2m_24h_min" IS '2米温度最小值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."tem_2m_24h_max" IS '2米温度最大值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."visib_24h" IS '能见度（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."pbl_24h" IS '行星边界层高度（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."pbl_24h_min" IS '行星边界层高度最小值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."pbl_24h_max" IS '行星边界层高度最大值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."windspeed_10m_24h" IS '10米风速（24小时平均）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."windspeed_10m_24h_min" IS '10米风速最小值（24小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."windspeed_10m_24h_max" IS '10米风速最大值（24小时）';

-- wh_meteorological_predict_hour_records
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."winddirect_10m_1h" IS '10米风向（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."winddirect8_10m_1h" IS '10米8方位风向（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."winddirect16_10m_1h" IS '10米16方位风向（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."windspeed_10m_1h" IS '10米风速（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."tem_2m_1h" IS '2米温度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."hum_2m_1h" IS '2米湿度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dewpoint_1h" IS '露点温度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dtem_2m_1h" IS '2米温度1小时变化';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dtem_2m_3h" IS '2米温度3小时变化';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dtem_2m_6h" IS '2米温度6小时变化';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dtem_2m_12h" IS '2米温度12小时变化';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."dtem_2m_24h" IS '2米温度24小时变化';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."rain_1h" IS '小时降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."rain_3h" IS '3小时累计降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."rain_6h" IS '6小时累计降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."rain_12h" IS '12小时累计降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."rain_24h" IS '24小时累计降雨量';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."lowcloud_1h" IS '低云量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."midcloud_1h" IS '中云量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."highcloud_1h" IS '高云量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."totalcloud_1h" IS '总云量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."pbl_1h" IS '行星边界层高度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."height_1h" IS '边界层高度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."pressure_1h" IS '海平面气压（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."stapress_1h" IS '地面气压（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."glw_1h" IS '长波辐射通量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."swdown_1h" IS '短波辐射通量（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."p850inver_1h" IS '850hPa逆温层高度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."p925inver_1h" IS '925hPa逆温层高度（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."visib_1h" IS '能见度（小时）';

-- wm_hydrological_info
COMMENT ON COLUMN public."wm_hydrological_info"."last_maintenance_time" IS '最近维护时间';

-- wm_meteorological_info
COMMENT ON COLUMN public."wm_meteorological_info"."last_maintenance_time" IS '最近维护时间';

-- wm_raster_inversion_config
COMMENT ON COLUMN public."wm_raster_inversion_config"."type_code" IS '反演类型编码';

-- wm_station_info
COMMENT ON COLUMN public."wm_station_info"."last_maintenance_time" IS '最近维护时间';

-- wm_waterbody_info
COMMENT ON COLUMN public."wm_waterbody_info"."water_body_function" IS '水体功能类别';
COMMENT ON COLUMN public."wm_waterbody_info"."basin" IS '所在流域';
COMMENT ON COLUMN public."wm_waterbody_info"."start_village" IS '起点村/社区';
COMMENT ON COLUMN public."wm_waterbody_info"."end_village" IS '终点村/社区';
COMMENT ON COLUMN public."wm_waterbody_info"."up_stream" IS '上游水体';
COMMENT ON COLUMN public."wm_waterbody_info"."down_stream" IS '下游水体';

-- wst_asset_trace_snap
COMMENT ON COLUMN public."wst_asset_trace_snap"."snap_distance_m" IS '吸附距离（米）';

-- wst_asset_type_dict
COMMENT ON COLUMN public."wst_asset_type_dict"."asset_group" IS '资产分组编码';
COMMENT ON COLUMN public."wst_asset_type_dict"."asset_group_name" IS '资产分组名称';
COMMENT ON COLUMN public."wst_asset_type_dict"."group_sort" IS '分组排序号';
COMMENT ON COLUMN public."wst_asset_type_dict"."group_description" IS '分组描述';

-- wst_layer_river
COMMENT ON COLUMN public."wst_layer_river"."next_down" IS '下游河流ID';
COMMENT ON COLUMN public."wst_layer_river"."river_class" IS '河流类别';
COMMENT ON COLUMN public."wst_layer_river"."length_km" IS '河流长度（公里）';
COMMENT ON COLUMN public."wst_layer_river"."from_z" IS '起点高程';
COMMENT ON COLUMN public."wst_layer_river"."to_z" IS '终点高程';

-- wst_trace_edge
COMMENT ON COLUMN public."wst_trace_edge"."direction_status" IS '流向状态';

-- wst_trace_topology_issue
COMMENT ON COLUMN public."wst_trace_topology_issue"."issue_type" IS '问题类型';
COMMENT ON COLUMN public."wst_trace_topology_issue"."issue_name" IS '问题名称';
COMMENT ON COLUMN public."wst_trace_topology_issue"."issue_level" IS '问题级别';
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_type" IS '关联对象类型';
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_id" IS '关联对象ID';
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_name" IS '关联对象名称';
COMMENT ON COLUMN public."wst_trace_topology_issue"."issue_desc" IS '问题详细描述';
COMMENT ON COLUMN public."wst_trace_topology_issue"."metadata_json" IS '元数据JSON';

-- ==========================================
-- A_auto_safe 注释批量 SQL 草案
-- 生成时间: 2026-07-08
-- 状态: 草案，待人工执行前最终确认，未执行
-- 字段候选: 299 条
-- 表候选:   13 条
-- 抽样校验: 40 条通过，0 条降级
-- 警告: 执行前需人工检查对象存在性
-- ==========================================

-- === 表级注释 ===

COMMENT ON TABLE public."gis_control_unit" IS '水环境管控单元表';
COMMENT ON TABLE public."gis_ecologicalregion" IS '生态保护红线区域表';
COMMENT ON TABLE public."gis_headwaters" IS '水源地表';
COMMENT ON TABLE public."gis_naturereserve" IS '自然保护区表';
COMMENT ON TABLE public."gis_region_city" IS '城市行政区划表';
COMMENT ON TABLE public."gis_region_population" IS '行政区人口统计表';
COMMENT ON TABLE public."gis_watershed_partition_3" IS '三级流域分区表';
COMMENT ON TABLE public."gis_watershed_partition_4" IS '四级流域分区表';
COMMENT ON TABLE public."layer_river_provincial" IS '省级河流空间表';
COMMENT ON TABLE public."wm_raster_info" IS '遥感影像栅格信息表';
COMMENT ON TABLE public."wm_raster_inversion_config" IS '遥感反演配置表';
COMMENT ON TABLE public."wst_layer_river" IS '溯源图层河流表';
COMMENT ON TABLE public."wst_trace_topology_issue" IS '溯源拓扑问题记录表';

-- === 字段级注释 ===

-- _stg_yichang_river_import
COMMENT ON COLUMN public."_stg_yichang_river_import"."gid" IS '地理要素唯一标识';
COMMENT ON COLUMN public."_stg_yichang_river_import"."OBJECTID" IS '对象唯一标识';
COMMENT ON COLUMN public."_stg_yichang_river_import"."geom" IS '空间几何数据';

-- _stg_yichang_river_std
COMMENT ON COLUMN public."_stg_yichang_river_std"."gid" IS '地理要素唯一标识';
COMMENT ON COLUMN public."_stg_yichang_river_std"."river_code" IS '河流编码';
COMMENT ON COLUMN public."_stg_yichang_river_std"."river_name" IS '河流名称';
COMMENT ON COLUMN public."_stg_yichang_river_std"."geom" IS '空间几何数据';

-- ad_dict
COMMENT ON COLUMN public."ad_dict"."create_time" IS '创建时间';
COMMENT ON COLUMN public."ad_dict"."update_time" IS '修改时间';
COMMENT ON COLUMN public."ad_dict"."del_flag" IS '删除标志：0-正常，1-已删除';
COMMENT ON COLUMN public."ad_dict"."create_by" IS '创建人';
COMMENT ON COLUMN public."ad_dict"."update_by" IS '修改人';

-- gis_ecologicalregion
COMMENT ON COLUMN public."gis_ecologicalregion"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_ecologicalregion"."ecological_region_name" IS '生态红线区域名称';
COMMENT ON COLUMN public."gis_ecologicalregion"."ecological_region_code" IS '生态红线区域编码';
COMMENT ON COLUMN public."gis_ecologicalregion"."address" IS '地址';
COMMENT ON COLUMN public."gis_ecologicalregion"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."gis_ecologicalregion"."population" IS '人口数量';
COMMENT ON COLUMN public."gis_ecologicalregion"."type" IS '类型';
COMMENT ON COLUMN public."gis_ecologicalregion"."remark" IS '备注';
COMMENT ON COLUMN public."gis_ecologicalregion"."create_by" IS '创建人';
COMMENT ON COLUMN public."gis_ecologicalregion"."create_time" IS '创建时间';
COMMENT ON COLUMN public."gis_ecologicalregion"."update_by" IS '修改人';
COMMENT ON COLUMN public."gis_ecologicalregion"."update_time" IS '修改时间';
COMMENT ON COLUMN public."gis_ecologicalregion"."del_flag" IS '删除标志：0-正常，1-已删除';

-- gis_headwaters
COMMENT ON COLUMN public."gis_headwaters"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_headwaters"."headwaters_name" IS '水源地名称';
COMMENT ON COLUMN public."gis_headwaters"."headwaters_code" IS '水源地编码';
COMMENT ON COLUMN public."gis_headwaters"."address" IS '地址';
COMMENT ON COLUMN public."gis_headwaters"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."gis_headwaters"."level" IS '级别';
COMMENT ON COLUMN public."gis_headwaters"."type" IS '类型';
COMMENT ON COLUMN public."gis_headwaters"."remark" IS '备注';
COMMENT ON COLUMN public."gis_headwaters"."create_by" IS '创建人';
COMMENT ON COLUMN public."gis_headwaters"."create_time" IS '创建时间';
COMMENT ON COLUMN public."gis_headwaters"."update_by" IS '修改人';
COMMENT ON COLUMN public."gis_headwaters"."update_time" IS '修改时间';
COMMENT ON COLUMN public."gis_headwaters"."del_flag" IS '删除标志：0-正常，1-已删除';

-- gis_naturereserve
COMMENT ON COLUMN public."gis_naturereserve"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_naturereserve"."nature_reserve_name" IS '自然保护区名称';
COMMENT ON COLUMN public."gis_naturereserve"."nature_reserve_code" IS '自然保护区编码';
COMMENT ON COLUMN public."gis_naturereserve"."address" IS '地址';
COMMENT ON COLUMN public."gis_naturereserve"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."gis_naturereserve"."type" IS '类型';
COMMENT ON COLUMN public."gis_naturereserve"."level" IS '级别';
COMMENT ON COLUMN public."gis_naturereserve"."population" IS '人口数量';
COMMENT ON COLUMN public."gis_naturereserve"."create_by" IS '创建人';
COMMENT ON COLUMN public."gis_naturereserve"."create_time" IS '创建时间';
COMMENT ON COLUMN public."gis_naturereserve"."update_by" IS '修改人';
COMMENT ON COLUMN public."gis_naturereserve"."update_time" IS '修改时间';
COMMENT ON COLUMN public."gis_naturereserve"."del_flag" IS '删除标志：0-正常，1-已删除';

-- gis_poi
COMMENT ON COLUMN public."gis_poi"."create_time" IS '创建时间';
COMMENT ON COLUMN public."gis_poi"."update_time" IS '修改时间';
COMMENT ON COLUMN public."gis_poi"."del_flag" IS '删除标志：0-正常，1-已删除';
COMMENT ON COLUMN public."gis_poi"."create_by" IS '创建人';
COMMENT ON COLUMN public."gis_poi"."update_by" IS '修改人';

-- gis_region
COMMENT ON COLUMN public."gis_region"."region_code" IS '行政区划编码';
COMMENT ON COLUMN public."gis_region"."region_name" IS '行政区划名称';
COMMENT ON COLUMN public."gis_region"."control_unit_id" IS '管控单元ID';
COMMENT ON COLUMN public."gis_region"."code" IS '编码';
COMMENT ON COLUMN public."gis_region"."address" IS '地址';
COMMENT ON COLUMN public."gis_region"."remark" IS '备注';

-- gis_region_city
COMMENT ON COLUMN public."gis_region_city"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_region_city"."geom" IS '空间几何数据';

-- gis_region_county
COMMENT ON COLUMN public."gis_region_county"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_region_county"."geom" IS '空间几何数据';

-- gis_region_population
COMMENT ON COLUMN public."gis_region_population"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_region_population"."region_id" IS '区域ID';
COMMENT ON COLUMN public."gis_region_population"."year" IS '年份';
COMMENT ON COLUMN public."gis_region_population"."create_by" IS '创建人';
COMMENT ON COLUMN public."gis_region_population"."create_time" IS '创建时间';
COMMENT ON COLUMN public."gis_region_population"."update_by" IS '修改人';
COMMENT ON COLUMN public."gis_region_population"."update_time" IS '修改时间';
COMMENT ON COLUMN public."gis_region_population"."del_flag" IS '删除标志：0-正常，1-已删除';

-- gis_region_township
COMMENT ON COLUMN public."gis_region_township"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_region_township"."geom" IS '空间几何数据';

-- gis_watershed_partition
COMMENT ON COLUMN public."gis_watershed_partition"."id" IS '主键ID';

-- gis_watershed_partition_3
COMMENT ON COLUMN public."gis_watershed_partition_3"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_watershed_partition_3"."geom" IS '空间几何数据';

-- gis_watershed_partition_4
COMMENT ON COLUMN public."gis_watershed_partition_4"."id" IS '主键ID';
COMMENT ON COLUMN public."gis_watershed_partition_4"."geom" IS '空间几何数据';

-- layer_boundary_enterprise
COMMENT ON COLUMN public."layer_boundary_enterprise"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_boundary_enterprise"."name" IS '名称';
COMMENT ON COLUMN public."layer_boundary_enterprise"."code" IS '编码';
COMMENT ON COLUMN public."layer_boundary_enterprise"."geom" IS '空间几何数据';

-- layer_boundary_park
COMMENT ON COLUMN public."layer_boundary_park"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_boundary_park"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_boundary_park"."name" IS '名称';
COMMENT ON COLUMN public."layer_boundary_park"."code" IS '编码';

-- layer_industrial_ghysgw
COMMENT ON COLUMN public."layer_industrial_ghysgw"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_ghysgw"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_ghysgw"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_ghysgw"."code" IS '编码';

-- layer_industrial_lsf
COMMENT ON COLUMN public."layer_industrial_lsf"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_lsf"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_lsf"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_lsf"."code" IS '编码';

-- layer_industrial_xzysgw
COMMENT ON COLUMN public."layer_industrial_xzysgw"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_xzysgw"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_xzysgw"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_xzysgw"."code" IS '编码';

-- layer_industrial_yjf
COMMENT ON COLUMN public."layer_industrial_yjf"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_yjf"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_yjf"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_yjf"."code" IS '编码';

-- layer_industrial_yjsgc
COMMENT ON COLUMN public."layer_industrial_yjsgc"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_yjsgc"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_yjsgc"."x" IS 'X坐标';
COMMENT ON COLUMN public."layer_industrial_yjsgc"."y" IS 'Y坐标';
COMMENT ON COLUMN public."layer_industrial_yjsgc"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_yjsgc"."code" IS '编码';

-- layer_industrial_ysc
COMMENT ON COLUMN public."layer_industrial_ysc"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_industrial_ysc"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_industrial_ysc"."x" IS 'X坐标';
COMMENT ON COLUMN public."layer_industrial_ysc"."y" IS 'Y坐标';
COMMENT ON COLUMN public."layer_industrial_ysc"."name" IS '名称';
COMMENT ON COLUMN public."layer_industrial_ysc"."code" IS '编码';

-- layer_outlet_sewage
COMMENT ON COLUMN public."layer_outlet_sewage"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_outlet_sewage"."x" IS 'X坐标';
COMMENT ON COLUMN public."layer_outlet_sewage"."y" IS 'Y坐标';
COMMENT ON COLUMN public."layer_outlet_sewage"."name" IS '名称';
COMMENT ON COLUMN public."layer_outlet_sewage"."code" IS '编码';
COMMENT ON COLUMN public."layer_outlet_sewage"."geom" IS '空间几何数据';

-- layer_partition_2
COMMENT ON COLUMN public."layer_partition_2"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_partition_2"."geom" IS '空间几何数据';

-- layer_partition_3
COMMENT ON COLUMN public."layer_partition_3"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_partition_3"."geom" IS '空间几何数据';

-- layer_reservoir_provincial
COMMENT ON COLUMN public."layer_reservoir_provincial"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_reservoir_provincial"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_reservoir_provincial"."objectid" IS '对象唯一标识';
COMMENT ON COLUMN public."layer_reservoir_provincial"."name" IS '名称';
COMMENT ON COLUMN public."layer_reservoir_provincial"."type" IS '类型';
COMMENT ON COLUMN public."layer_reservoir_provincial"."length" IS '长度';

-- layer_reservoir_provincial_label
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."name" IS '名称';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."type" IS '类型';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."length" IS '长度';
COMMENT ON COLUMN public."layer_reservoir_provincial_label"."id" IS '主键ID';

-- layer_reservoir_provincial_合并
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."name" IS '名称';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."type" IS '类型';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."length" IS '长度';
COMMENT ON COLUMN public."layer_reservoir_provincial_合并"."id" IS '主键ID';

-- layer_river_provincial
COMMENT ON COLUMN public."layer_river_provincial"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_river_provincial"."type" IS '类型';
COMMENT ON COLUMN public."layer_river_provincial"."length" IS '长度';
COMMENT ON COLUMN public."layer_river_provincial"."width" IS '宽度';
COMMENT ON COLUMN public."layer_river_provincial"."name" IS '名称';
COMMENT ON COLUMN public."layer_river_provincial"."id" IS '主键ID';

-- layer_river_provincial_bak0617
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."type" IS '类型';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."length" IS '长度';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."width" IS '宽度';
COMMENT ON COLUMN public."layer_river_provincial_bak0617"."name" IS '名称';

-- layer_section
COMMENT ON COLUMN public."layer_section"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_section"."x" IS 'X坐标';
COMMENT ON COLUMN public."layer_section"."y" IS 'Y坐标';
COMMENT ON COLUMN public."layer_section"."name" IS '名称';
COMMENT ON COLUMN public."layer_section"."code" IS '编码';
COMMENT ON COLUMN public."layer_section"."geom" IS '空间几何数据';

-- layer_watershed
COMMENT ON COLUMN public."layer_watershed"."id" IS '主键ID';
COMMENT ON COLUMN public."layer_watershed"."name" IS '名称';
COMMENT ON COLUMN public."layer_watershed"."code" IS '编码';
COMMENT ON COLUMN public."layer_watershed"."geom" IS '空间几何数据';

-- metadata_view
COMMENT ON COLUMN public."metadata_view"."code" IS '编码';
COMMENT ON COLUMN public."metadata_view"."parent_id" IS '父级ID';
COMMENT ON COLUMN public."metadata_view"."type" IS '类型';

-- rs_industrial_info_yc
COMMENT ON COLUMN public."rs_industrial_info_yc"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_industrial_info_yc"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_industrial_info_yc"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_industrial_info_yc"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_industrial_info_yc"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_industrial_info_yc_bak0305
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_industrial_info_yc_bak0305"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_outlet_info_v2
COMMENT ON COLUMN public."rs_outlet_info_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_outlet_info_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_outlet_info_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_outlet_info_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_outlet_info_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_outlet_info_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_outlet_live_v2
COMMENT ON COLUMN public."rs_outlet_live_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_outlet_live_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_outlet_live_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_outlet_live_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_outlet_live_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_outlet_live_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_outlet_monitor_v2
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_outlet_monitor_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_outlet_remediation_v2
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_outlet_remediation_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_outlet_trace_v2
COMMENT ON COLUMN public."rs_outlet_trace_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_outlet_trace_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_outlet_trace_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_outlet_trace_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_outlet_trace_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_outlet_trace_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_sewage_info_v2
COMMENT ON COLUMN public."rs_sewage_info_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."rs_sewage_info_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_sewage_info_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_sewage_info_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_sewage_info_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_sewage_info_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- rs_sewage_park_info
COMMENT ON COLUMN public."rs_sewage_park_info"."create_by" IS '创建人';
COMMENT ON COLUMN public."rs_sewage_park_info"."create_time" IS '创建时间';
COMMENT ON COLUMN public."rs_sewage_park_info"."update_by" IS '修改人';
COMMENT ON COLUMN public."rs_sewage_park_info"."update_time" IS '修改时间';
COMMENT ON COLUMN public."rs_sewage_park_info"."del_flag" IS '删除标志：0-正常，1-已删除';

-- se_watershed
COMMENT ON COLUMN public."se_watershed"."id" IS '主键ID';

-- spatial_ref_sys
COMMENT ON COLUMN public."spatial_ref_sys"."srid" IS '空间参考标识符';
COMMENT ON COLUMN public."spatial_ref_sys"."auth_name" IS '空间参考系授权机构名称';
COMMENT ON COLUMN public."spatial_ref_sys"."auth_srid" IS '空间参考系授权机构SRID';
COMMENT ON COLUMN public."spatial_ref_sys"."srtext" IS '空间参考系WKT描述';
COMMENT ON COLUMN public."spatial_ref_sys"."proj4text" IS '空间参考系Proj4描述';

-- stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df"."create_by" IS '创建人';
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df"."create_date" IS '创建日期';
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df"."update_by" IS '修改人';
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_anchorage_info_df"."update_date" IS '修改日期';

-- stg_sjtysj_cbwrwxtzlxxxt_b_receive_ship_assessment_df
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_receive_ship_assessment_df"."id" IS '主键ID';

-- stg_sjtysj_cbwrwxtzlxxxt_b_wharf_info_df
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_wharf_info_df"."id" IS '主键ID';
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_b_wharf_info_df"."geom" IS '空间几何数据';

-- stg_sjtysj_cbwrwxtzlxxxt_p_handover_trans_detail_df
COMMENT ON COLUMN public."stg_sjtysj_cbwrwxtzlxxxt_p_handover_trans_detail_df"."create_time" IS '创建时间';

-- stg_ycsjtysj_sxhyzssj_base_ship_df
COMMENT ON COLUMN public."stg_ycsjtysj_sxhyzssj_base_ship_df"."create_time" IS '创建时间';
COMMENT ON COLUMN public."stg_ycsjtysj_sxhyzssj_base_ship_df"."update_time" IS '修改时间';

-- wh_meteorological_predict_day_records
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."predictiontime" IS '预测时间';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."predictioninterval" IS '预测间隔（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_day_records"."datadate" IS '数据日期';

-- wh_meteorological_predict_hour_records
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."predictiontime" IS '预测时间';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."predictioninterval" IS '预测间隔（小时）';
COMMENT ON COLUMN public."wh_meteorological_predict_hour_records"."datadate" IS '数据日期';

-- wm_camera_platform
COMMENT ON COLUMN public."wm_camera_platform"."id" IS '主键ID';

-- wm_hydrological_info
COMMENT ON COLUMN public."wm_hydrological_info"."region_code" IS '行政区划代码';
COMMENT ON COLUMN public."wm_hydrological_info"."geom" IS '空间几何数据';

-- wm_image_info
COMMENT ON COLUMN public."wm_image_info"."id" IS '主键ID';

-- wm_meteorological_info
COMMENT ON COLUMN public."wm_meteorological_info"."region_code" IS '行政区划代码';
COMMENT ON COLUMN public."wm_meteorological_info"."geom" IS '空间几何数据';

-- wm_raster_info
COMMENT ON COLUMN public."wm_raster_info"."id" IS '主键ID';

-- wm_raster_inversion
COMMENT ON COLUMN public."wm_raster_inversion"."id" IS '主键ID';

-- wm_raster_inversion_config
COMMENT ON COLUMN public."wm_raster_inversion_config"."id" IS '主键ID';
COMMENT ON COLUMN public."wm_raster_inversion_config"."name" IS '名称';
COMMENT ON COLUMN public."wm_raster_inversion_config"."create_time" IS '创建时间';
COMMENT ON COLUMN public."wm_raster_inversion_config"."update_time" IS '修改时间';
COMMENT ON COLUMN public."wm_raster_inversion_config"."del_flag" IS '删除标志：0-正常，1-已删除';

-- wm_station_info
COMMENT ON COLUMN public."wm_station_info"."region_code" IS '行政区划代码';
COMMENT ON COLUMN public."wm_station_info"."geom" IS '空间几何数据';

-- wm_station_info_v2
COMMENT ON COLUMN public."wm_station_info_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."wm_station_info_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."wm_station_info_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."wm_station_info_v2"."update_time" IS '修改时间';

-- wm_uav_info
COMMENT ON COLUMN public."wm_uav_info"."id" IS '主键ID';

-- wm_water_intake
COMMENT ON COLUMN public."wm_water_intake"."id" IS '主键ID';
COMMENT ON COLUMN public."wm_water_intake"."geom" IS '空间几何数据';

-- wm_water_source
COMMENT ON COLUMN public."wm_water_source"."id" IS '主键ID';
COMMENT ON COLUMN public."wm_water_source"."geom" IS '空间几何数据';

-- wm_water_source_bak0421
COMMENT ON COLUMN public."wm_water_source_bak0421"."id" IS '主键ID';

-- wm_water_source_intake_v2
COMMENT ON COLUMN public."wm_water_source_intake_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."wm_water_source_intake_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."wm_water_source_intake_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."wm_water_source_intake_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."wm_water_source_intake_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."wm_water_source_intake_v2"."del_flag" IS '删除标志：0-正常，1-已删除';

-- wm_water_source_zone_v2
COMMENT ON COLUMN public."wm_water_source_zone_v2"."id" IS '主键ID';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."create_by" IS '创建人';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."create_time" IS '创建时间';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."update_by" IS '修改人';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."update_time" IS '修改时间';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."del_flag" IS '删除标志：0-正常，1-已删除';
COMMENT ON COLUMN public."wm_water_source_zone_v2"."geom" IS '空间几何数据';

-- wm_waterbody_info
COMMENT ON COLUMN public."wm_waterbody_info"."water_body_code" IS '水体编码';
COMMENT ON COLUMN public."wm_waterbody_info"."remark" IS '备注';

-- wm_waterquality_day_records
COMMENT ON COLUMN public."wm_waterquality_day_records"."status" IS '状态';

-- wst_asset_trace_snap
COMMENT ON COLUMN public."wst_asset_trace_snap"."snap_node_id" IS '吸附节点ID';
COMMENT ON COLUMN public."wst_asset_trace_snap"."snap_edge_id" IS '吸附边ID';
COMMENT ON COLUMN public."wst_asset_trace_snap"."status" IS '状态';

-- wst_layer_river
COMMENT ON COLUMN public."wst_layer_river"."id" IS '主键ID';
COMMENT ON COLUMN public."wst_layer_river"."river_code" IS '河流编码';
COMMENT ON COLUMN public."wst_layer_river"."river_name" IS '河流名称';
COMMENT ON COLUMN public."wst_layer_river"."geom" IS '空间几何数据';

-- wst_trace_edge
COMMENT ON COLUMN public."wst_trace_edge"."source_asset_id" IS '源资产ID';
COMMENT ON COLUMN public."wst_trace_edge"."from_node_id" IS '上游节点ID';
COMMENT ON COLUMN public."wst_trace_edge"."to_node_id" IS '下游节点ID';

-- wst_trace_node
COMMENT ON COLUMN public."wst_trace_node"."asset_id" IS '资产ID';

-- wst_trace_topology_issue
COMMENT ON COLUMN public."wst_trace_topology_issue"."id" IS '主键ID';
COMMENT ON COLUMN public."wst_trace_topology_issue"."status" IS '状态';
COMMENT ON COLUMN public."wst_trace_topology_issue"."geom" IS '空间几何数据';
COMMENT ON COLUMN public."wst_trace_topology_issue"."remark" IS '备注';
COMMENT ON COLUMN public."wst_trace_topology_issue"."del_flag" IS '删除标志：0-正常，1-已删除';

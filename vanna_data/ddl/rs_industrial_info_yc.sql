-- Table: public."rs_industrial_info_yc"
-- Table comment: 工业园区环境监测数据表
CREATE TABLE public."rs_industrial_info_yc" (
  "id" bigint,
  "name" character varying(255),
  "name_part" character varying(255),
  "region_code" character varying(20),
  "region_name" character varying(100),
  "park_level" integer,
  "lon" double precision,
  "lat" double precision,
  "belong_watershed" character varying(255),
  "is_within_1km_yangtze_mainstream" character varying(255),
  "is_within_1km_yangtze_tributary" character varying(255),
  "important_tributary" character varying(255),
  "is_chemical_park" character varying(255),
  "park_development_status" character varying(255),
  "leading_industry" text,
  "total_industrial_output_value_10k_yuan" character varying(255),
  "industrial_value_added_10k_yuan" character varying(255),
  "industrial_land_area_sqkm" character varying(255),
  "enterprises_above_designated_count" character varying(255),
  "cumulative_investment_wastewater_treatment_10k_yuan" character varying(255),
  "cumulative_investment_sewer_network_10k_yuan" character varying(255),
  "sewer_network_length_km" character varying(255),
  "new_sewer_network_length_km" character varying(255),
  "park_drainage_status" character varying(255),
  "sewer_inspection_rectification_since_2020" text,
  "sewer_inspection_length_km" character varying(255),
  "treatment_facility_name" character varying(255),
  "pollution_discharge_permit_code" character varying(255),
  "treatment_facility_type" character varying(255),
  "treatment_cost_yuan_per_ton" character varying(255),
  "is_industrial_wastewater_pipe_access_assessment" character varying(255),
  "designed_treatment_capacity_10k_tons_per_day" character varying(255),
  "actual_treatment_volume_10k_tons" character varying(255),
  "treatment_process_name" character varying(255),
  "emission_standard" character varying(255),
  "designed_influent_cod_mg_l" character varying(255),
  "designed_influent_ammonia_nitrogen_mg_l" character varying(255),
  "influent_cod_daily_avg_mg_l" character varying(255),
  "influent_ammonia_nitrogen_daily_avg_mg_l" character varying(255),
  "influent_total_nitrogen_daily_avg_mg_l" character varying(255),
  "influent_total_phosphorus_daily_avg_mg_l" character varying(255),
  "effluent_cod_daily_avg_mg_l" character varying(255),
  "effluent_ammonia_nitrogen_daily_avg_mg_l" character varying(255),
  "effluent_total_nitrogen_daily_avg_mg_l" character varying(255),
  "effluent_total_phosphorus_daily_avg_mg_l" character varying(255),
  "is_key_pollution_source" character varying(255),
  "ecology_dept_networking_influent_effluent" character varying(255),
  "auto_monitoring_system_level" character varying(255),
  "auto_monitoring_compliance_rate_pct" character varying(255),
  "manual_monitoring_compliance_rate_pct" character varying(255),
  "exceedance_factor_and_multiplier" character varying(255),
  "exceedance_days" character varying(255),
  "exceedance_reason" text,
  "treatment_plant_power_consumption_kwh" character varying(255),
  "is_photovoltaic_station_built" character varying(255),
  "chemical_addition_type" character varying(255),
  "chemical_addition_quantity_tons" character varying(255),
  "is_precision_aeration" character varying(255),
  "is_negotiated_pipe_access_standard" character varying(255),
  "system_issues" text,
  "rectification_status" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键
--   name: 名称
--   name_part: 分园名称
--   region_code: 行政区划编码
--   region_name: 行政区名称
--   park_level: 园区级别：0-未知、1-国家级、2-省级、3-市级
--   lon: 经度
--   lat: 纬度
--   belong_watershed: 所属流域
--   is_within_1km_yangtze_mainstream: 是否在长江干流岸线一公里范围内
--   is_within_1km_yangtze_tributary: 是否在长江重要支流岸线一公里范围内
--   important_tributary: 所属重要支流
--   is_chemical_park: 是否为化工园区
--   park_development_status: 园区发展现状
--   leading_industry: 主导产业
--   total_industrial_output_value_10k_yuan: 调度期内工业总产值（万元）
--   industrial_value_added_10k_yuan: 调度期内工业增加值（万元）
--   industrial_land_area_sqkm: 工业用地面积（平方千米）
--   enterprises_above_designated_count: 规上企业数量（个）
--   cumulative_investment_wastewater_treatment_10k_yuan: 工业园区对污水集中处理设施累计投资（万元）
--   cumulative_investment_sewer_network_10k_yuan: 工业园区对污水管网累计投资（万元）
--   sewer_network_length_km: 污水管网长度（千米）
--   new_sewer_network_length_km: 新增管网长度（千米）
--   park_drainage_status: 工业园区排水现状
--   sewer_inspection_rectification_since_2020: 2020年以来污水管网排查整治情况管网排查情况
--   sewer_inspection_length_km: 管网排查长度（千米）
--   treatment_facility_name: 污水处理设施名称
--   pollution_discharge_permit_code: 排污许可证编码
--   treatment_facility_type: 污水处理设施类型
--   treatment_cost_yuan_per_ton: 吨水处理费用（元/吨）
--   is_industrial_wastewater_pipe_access_assessment: （排入城镇污水集中处理设施）是否开展园区工业废水纳管评估
--   designed_treatment_capacity_10k_tons_per_day: 设计处理能力（万吨/日）
--   actual_treatment_volume_10k_tons: 实际处理水量（万吨）
--   treatment_process_name: 污水处理工艺名称
--   emission_standard: 执行排放标准
--   designed_influent_cod_mg_l: 设计进水浓度（COD）
--   designed_influent_ammonia_nitrogen_mg_l: 设计进水浓度（氨氮）
--   influent_cod_daily_avg_mg_l: 进水COD日均值（mg/L）
--   influent_ammonia_nitrogen_daily_avg_mg_l: 进水氨氮日均值（mg/L）
--   influent_total_nitrogen_daily_avg_mg_l: 进水总氮日均值（mg/L）
--   influent_total_phosphorus_daily_avg_mg_l: 进水总磷日均值（mg/L）
--   effluent_cod_daily_avg_mg_l: 出水COD日均值（mg/L）
--   effluent_ammonia_nitrogen_daily_avg_mg_l: 出水氨氮日均值（mg/L）
--   effluent_total_nitrogen_daily_avg_mg_l: 出水总氮日均值（mg/L）
--   effluent_total_phosphorus_daily_avg_mg_l: 出水总磷日均值（mg/L）
--   is_key_pollution_source: 是否重点排污单位
--   ecology_dept_networking_influent_effluent: 与生态环境部门联网情况（进出水）
--   auto_monitoring_system_level: 重点污染源自动监控系统（部、省、市、县）
--   auto_monitoring_compliance_rate_pct: 自动在线监控达标率（%）
--   manual_monitoring_compliance_rate_pct: 手工监测达标率（%）
--   exceedance_factor_and_multiplier: 超标因子及超标倍数
--   exceedance_days: 超标天数
--   exceedance_reason: 超标原因
--   treatment_plant_power_consumption_kwh: 污水厂耗电量
--   is_photovoltaic_station_built: 是否建设光伏电站
--   chemical_addition_type: 药剂添加类型
--   chemical_addition_quantity_tons: 药剂添加数量（吨）
--   is_precision_aeration: 是否精准曝气
--   is_negotiated_pipe_access_standard: 园区企业与污水处理厂是否协商制定纳管标准
--   system_issues: 系统上存在的问题
--   rectification_status: 整改情况
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

-- Table: public."rs_sewage_info_v2"
-- Table comment: 污水处理厂档案管理及监测
CREATE TABLE public."rs_sewage_info_v2" (
  "id" bigint NOT NULL DEFAULT nextval('archive_wwtp_id_seq'::regclass),
  "admin_division" character varying(200),
  "project_name" character varying(200),
  "run_status" character varying(50),
  "treatment_process" character varying(200),
  "project_location_lng" numeric(12,6),
  "project_location_lat" numeric(12,6),
  "outlet_total_lng" numeric(12,6),
  "outlet_total_lat" numeric(12,6),
  "design_scale" numeric(12,2),
  "actual_assess_scale" numeric(12,2),
  "load_rate" numeric(6,2),
  "influent_flow" numeric(12,2),
  "influent_cod" numeric(12,4),
  "influent_ph" numeric(6,2),
  "influent_ammonia" numeric(12,4),
  "influent_tp" numeric(12,4),
  "influent_tn" numeric(12,4),
  "effluent_flow" numeric(12,2),
  "effluent_cod" numeric(12,4),
  "effluent_ph" numeric(6,2),
  "effluent_ammonia" numeric(12,4),
  "effluent_tp" numeric(12,4),
  "effluent_tn" numeric(12,4),
  "cod_daily_reduction" numeric(12,4),
  "cod_annual_reduction" numeric(12,4),
  "pipe_total_length" numeric(12,2),
  "well_count" integer,
  "pump_station_count" integer,
  "enterprise_total" integer,
  "connected_enterprise" integer,
  "connection_rate" numeric(6,2),
  "enterprise_drainage" numeric(12,2),
  "key_pollution_enterprise" integer,
  "online_monitor_enterprise" integer,
  "monitor_coverage_rate" numeric(6,2),
  "monthly_fee_total" numeric(12,2),
  "should_collect_enterprise" integer,
  "actual_collect_enterprise" integer,
  "collection_rate" numeric(6,2),
  "operation_unit" character varying(200),
  "plan_total_invest" numeric(14,2),
  "plan_station_invest" numeric(14,2),
  "plan_pipe_invest" numeric(14,2),
  "done_total_invest" numeric(14,2),
  "done_station_invest" numeric(14,2),
  "done_pipe_invest" numeric(14,2),
  "total_invest_rate" numeric(6,2),
  "built_pipe_length" numeric(12,2),
  "collection_rate_efficiency" numeric(6,2),
  "treatment_rate" numeric(6,2),
  "compliance_rate" numeric(6,2),
  "operation_load_rate" numeric(6,2),
  "center_lng" numeric(12,6),
  "center_lat" numeric(12,6),
  "total_outlet_lng" numeric(12,6),
  "total_outlet_lat" numeric(12,6),
  "tail_water_destination" character varying(200),
  "outlet_photo" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1) DEFAULT '0'::character varying
);

-- Column comments:
--   id: 主键ID
--   admin_division: 行政区划
--   project_name: 项目名称
--   run_status: 运行状态
--   treatment_process: 处理工艺
--   project_location_lng: 项目所在地经度
--   project_location_lat: 项目所在地纬度
--   outlet_total_lng: 污水总排放口经度
--   outlet_total_lat: 污水总排放口纬度
--   design_scale: 设计规模(t/d)
--   actual_assess_scale: 实际考核规模(t/d)
--   load_rate: 负荷率(%)
--   influent_flow: 进水流量(m3/d)
--   influent_cod: 进水COD(mg/L)
--   influent_ph: 进水pH
--   influent_ammonia: 进水氨氮(mg/L)
--   influent_tp: 进水总磷(mg/L)
--   influent_tn: 进水总氮(mg/L)
--   effluent_flow: 出水流量(m3/d)
--   effluent_cod: 出水COD(mg/L)
--   effluent_ph: 出水pH
--   effluent_ammonia: 出水氨氮(mg/L)
--   effluent_tp: 出水总磷(mg/L)
--   effluent_tn: 出水总氮(mg/L)
--   cod_daily_reduction: COD日削减量(t/d)
--   cod_annual_reduction: COD年削减量(t/a)
--   pipe_total_length: 园区管网总长(km)
--   well_count: 管井数量(个)
--   pump_station_count: 提升泵站数量(个)
--   enterprise_total: 园区企业总数(家)
--   connected_enterprise: 已接入企业数(家)
--   connection_rate: 接入率(%)
--   enterprise_drainage: 企业排水总量(m3/d)
--   key_pollution_enterprise: 重点排污企业数(家)
--   online_monitor_enterprise: 在线监测企业数(家)
--   monitor_coverage_rate: 监测覆盖率(%)
--   monthly_fee_total: 月污水处理费总额(元)
--   should_collect_enterprise: 应征企业数(家)
--   actual_collect_enterprise: 实征企业数(家)
--   collection_rate: 征收率(%)
--   operation_unit: 运营单位
--   plan_total_invest: 计划总投资(万元)
--   plan_station_invest: 计划厂站投资(万元)
--   plan_pipe_invest: 计划管网投资(万元)
--   done_total_invest: 已完成总投资(万元)
--   done_station_invest: 已完成厂站投资(万元)
--   done_pipe_invest: 已完成管网投资(万元)
--   total_invest_rate: 总投资完成率(%)
--   built_pipe_length: 已建管网长度(km)
--   collection_rate_efficiency: 污水收集率(%)
--   treatment_rate: 污水处理率(%)
--   compliance_rate: 达标排放率(%)
--   operation_load_rate: 运行负荷率(%)
--   center_lng: 企业中心经度
--   center_lat: 企业中心纬度
--   total_outlet_lng: 污水处理设施总排口经度
--   total_outlet_lat: 污水处理设施总排口纬度
--   tail_water_destination: 尾水排放去向
--   outlet_photo: 排口照片
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

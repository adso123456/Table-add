-- Table: public."rs_outlet_monitor_v2"
-- Table comment: 排污口监测
CREATE TABLE public."rs_outlet_monitor_v2" (
  "id" bigint NOT NULL DEFAULT nextval('archive_outlet_monitor_id_seq'::regclass),
  "outlet_id" bigint NOT NULL,
  "sampling_time" timestamp without time zone,
  "monitor_type" character varying(100),
  "flow" numeric(12,2),
  "water_temp" numeric(6,2),
  "bod" numeric(12,4),
  "cod" numeric(12,4),
  "ph" numeric(6,2),
  "ammonia_nitrogen" numeric(12,4),
  "total_phosphorus" numeric(12,4),
  "total_nitrogen" numeric(12,4),
  "remark" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1) DEFAULT '0'::character varying,
  "outlet_name" character varying(200)
);

-- Column comments:
--   id: 主键ID
--   outlet_id: 关联排污口ID
--   sampling_time: 采样时间
--   monitor_type: 监测类型
--   flow: 流量(立方米/天)
--   water_temp: 水温(℃)
--   bod: BOD(mg/L)
--   cod: COD(mg/L)
--   ph: pH
--   ammonia_nitrogen: 氨氮(mg/L)
--   total_phosphorus: 总磷(mg/L)
--   total_nitrogen: 总氮(mg/L)
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   outlet_name: 排污口名称

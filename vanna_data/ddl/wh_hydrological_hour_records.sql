-- Table: public."wh_hydrological_hour_records"
-- Table comment: 水文监测小时记录表
CREATE TABLE public."wh_hydrological_hour_records" (
  "id" bigint,
  "station_id" bigint,
  "m1_value" double precision,
  "m2_value" double precision,
  "m3_value" double precision,
  "m4_value" double precision,
  "m5_value" double precision,
  "m6_value" double precision,
  "m7_value" double precision,
  "m8_value" double precision,
  "m9_value" double precision,
  "m10_value" double precision,
  "record_type" character(1),
  "monitor_time" timestamp without time zone,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: id
--   station_id: 所属站点id
--   m1_value: 水深（单位米）
--   m2_value: 流速（单位m/s）
--   m3_value: 流量（单位m3/s）
--   m4_value: m4_value
--   m5_value: m5_value
--   m6_value: m6_value
--   m7_value: m7_value
--   m8_value: m8_value
--   m9_value: m9_value
--   m10_value: m10_value
--   record_type: 记录类型：0 自动、1 手工
--   monitor_time: 监测时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

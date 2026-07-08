-- Table: public."wh_hydrological_day_records"
-- Table comment: 水文监测日记录表
CREATE TABLE public."wh_hydrological_day_records" (
  "id" bigint,
  "station_id" bigint,
  "m1_value" double precision,
  "m1_count" bigint,
  "m2_value" double precision,
  "m2_count" bigint,
  "m3_value" double precision,
  "m3_count" bigint,
  "m4_value" double precision,
  "m4_count" bigint,
  "m5_value" double precision,
  "m5_count" bigint,
  "m6_value" double precision,
  "m6_count" bigint,
  "m7_value" double precision,
  "m7_count" bigint,
  "m8_value" double precision,
  "m8_count" bigint,
  "m9_value" double precision,
  "m9_count" bigint,
  "m10_value" double precision,
  "m10_count" bigint,
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
--   m1_count: 记录数1
--   m2_value: 流速（单位m/s）
--   m2_count: 记录数2
--   m3_value: 流量（单位m3/s）
--   m3_count: 记录数3
--   m4_value: m4_value
--   m4_count: 记录数4
--   m5_value: m5_value
--   m5_count: 记录数5
--   m6_value: m6_value
--   m6_count: 记录数6
--   m7_value: m7_value
--   m7_count: 记录数7
--   m8_value: m8_value
--   m8_count: 记录数8
--   m9_value: m9_value
--   m9_count: 记录数9
--   m10_value: m10_value
--   m10_count: 记录数10
--   record_type: 记录类型：0 自动、1 手工
--   monitor_time: 监测时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

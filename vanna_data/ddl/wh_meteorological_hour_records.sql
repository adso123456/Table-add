-- Table: public."wh_meteorological_hour_records"
-- Table comment: 气象数据小时记录表
CREATE TABLE public."wh_meteorological_hour_records" (
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
  "m11_value" double precision,
  "m12_value" double precision,
  "m13_value" double precision,
  "m14_value" double precision,
  "m15_value" double precision,
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
--   m1_value: 风速（m/s）
--   m2_value: 风向
--   m3_value: 气压（hPa）
--   m4_value: 气温（℃）
--   m5_value: 相对湿度（%）
--   m6_value: 分钟降雨量（mm）
--   m7_value: 蒸发量（单位mm/m2）
--   m8_value: 小时降雨量（mm）
--   m9_value: 24小时降雨量（mm）
--   m10_value: 累计降雨量（mm）
--   m11_value: m11_value
--   m12_value: m12_value
--   m13_value: m13_value
--   m14_value: m14_value
--   m15_value: m15_value
--   record_type: 记录类型：0 自动、1 手工
--   monitor_time: 监测时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

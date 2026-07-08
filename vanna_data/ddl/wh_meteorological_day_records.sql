-- Table: public."wh_meteorological_day_records"
-- Table comment: 气象数据日记录表
CREATE TABLE public."wh_meteorological_day_records" (
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
  "m11_value" double precision,
  "m11_count" bigint,
  "m12_value" double precision,
  "m12_count" bigint,
  "m13_value" double precision,
  "m13_count" bigint,
  "m14_value" double precision,
  "m14_count" bigint,
  "m15_value" double precision,
  "m15_count" bigint,
  "rain_fall" double precision,
  "high_temp" double precision,
  "low_temp" double precision,
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
--   m1_value: 风速（单位m/s）
--   m1_count: 记录数1
--   m2_value: 风向
--   m2_count: 记录数2
--   m3_value: 气压（单位hPa）
--   m3_count: 记录数3
--   m4_value: 气温（单位℃）
--   m4_count: 记录数4
--   m5_value: 相对湿度（单位RH）
--   m5_count: 记录数5
--   m6_value: 雨量（单位mm/m2）
--   m6_count: 记录数6
--   m7_value: 蒸发量（单位mm/m2）
--   m7_count: 记录数7
--   m8_value: 小时降雨量（mm）
--   m8_count: 记录数8
--   m9_value: 24小时降雨量（mm）
--   m9_count: 记录数9
--   m10_value: 累计降雨量（mm）
--   m10_count: 记录数10
--   m11_value: m11_value
--   m11_count: 记录数11
--   m12_value: m12_value
--   m12_count: 记录数12
--   m13_value: m13_value
--   m13_count: 记录数13
--   m14_value: m14_value
--   m14_count: 记录数14
--   m15_value: m15_value
--   m15_count: 记录数15
--   rain_fall: 8-20时降水量（mm）
--   high_temp: 日最高气温（℃）
--   low_temp: 日最低气温（℃）
--   record_type: 记录类型：0 自动、1 手工
--   monitor_time: 监测时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

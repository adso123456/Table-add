-- Table: public."wm_waterquality_day_records"
-- Table comment: 水质监测日记录表
CREATE TABLE public."wm_waterquality_day_records" (
  "id" bigint NOT NULL,
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
  "m16_value" double precision,
  "m16_count" bigint,
  "m17_value" double precision,
  "m17_count" bigint,
  "m18_value" double precision,
  "m18_count" bigint,
  "m19_value" double precision,
  "m19_count" bigint,
  "m20_value" double precision,
  "m20_count" bigint,
  "m21_value" double precision,
  "m21_count" bigint,
  "m22_value" double precision,
  "m22_count" bigint,
  "m23_value" double precision,
  "m23_count" bigint,
  "m24_value" double precision,
  "m24_count" bigint,
  "m25_value" double precision,
  "m25_count" bigint,
  "m26_value" double precision,
  "m26_count" bigint,
  "m27_value" double precision,
  "m27_count" bigint,
  "m28_value" double precision,
  "m28_count" bigint,
  "m29_value" double precision,
  "m29_count" bigint,
  "m30_value" double precision,
  "m30_count" bigint,
  "m31_value" double precision,
  "m31_count" bigint,
  "monitor_time" timestamp without time zone,
  "status" character(1),
  "water_quality_level" character varying(20),
  "record_type" character(1),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: id
--   station_id: 站点id
--   m1_value: 水温监测值
--   m1_count: 记录数1
--   m2_value: PH监测值
--   m2_count: 记录数2
--   m3_value: 溶解氧监测值
--   m3_count: 记录数3
--   m4_value: 浊度监测值
--   m4_count: 记录数4
--   m5_value: 电导率监测值
--   m5_count: 记录数5
--   m6_value: 氨氮监测值
--   m6_count: 记录数6
--   m7_value: 高锰酸盐指数监测值
--   m7_count: 记录数7
--   m8_value: 总磷监测值
--   m8_count: 记录数8
--   m9_value: 总氮监测值
--   m9_count: 记录数9
--   m10_value: 化学需氧量监测值
--   m10_count: 记录数10
--   m11_value: 监测值
--   m11_count: 记录数11
--   m12_value: 监测值
--   m12_count: 记录数12
--   m13_value: 监测值
--   m13_count: 记录数13
--   m14_value: 监测值
--   m14_count: 记录数14
--   m15_value: 监测值
--   m15_count: 记录数15
--   m16_value: 监测值
--   m16_count: 记录数16
--   m17_value: 监测值
--   m17_count: 记录数17
--   m18_value: 监测值
--   m18_count: 记录数18
--   m19_value: 监测值
--   m19_count: 记录数19
--   m20_value: 监测值
--   m20_count: 记录数20
--   m21_value: 监测值
--   m21_count: 记录数21
--   m22_value: 监测值
--   m22_count: 记录数22
--   m23_value: 监测值
--   m23_count: 记录数23
--   m24_value: 监测值
--   m24_count: 记录数24
--   m25_value: 监测值
--   m25_count: 记录数25
--   m26_value: 监测值
--   m26_count: 记录数26
--   m27_value: 监测值
--   m27_count: 记录数27
--   m28_value: 监测值
--   m28_count: 记录数28
--   m29_value: 监测值29
--   m29_count: 记录数29
--   m30_value: 监测值30
--   m30_count: 记录数30
--   m31_value: 监测值31
--   m31_count: 记录数31
--   monitor_time: 监测时间
--   status: 状态
--   water_quality_level: 水质级别
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

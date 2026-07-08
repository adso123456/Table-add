-- Table: public."wm_waterquality_hour_records"
-- Table comment: 水质监测小时记录表
CREATE TABLE public."wm_waterquality_hour_records" (
  "id" bigint,
  "station_id" bigint,
  "m1_value" double precision,
  "m1_status" character(1),
  "m1_level" character varying(4),
  "m2_value" double precision,
  "m2_status" character(1),
  "m2_level" character varying(4),
  "m3_value" double precision,
  "m3_status" character(1),
  "m3_level" character varying(4),
  "m4_value" double precision,
  "m4_status" character(1),
  "m5_value" double precision,
  "m5_status" character(1),
  "m6_value" double precision,
  "m6_status" character(1),
  "m6_level" character varying(4),
  "m7_value" double precision,
  "m7_status" character(1),
  "m7_level" character varying(4),
  "m8_value" double precision,
  "m8_status" character(1),
  "m8_level" character varying(4),
  "m9_value" double precision,
  "m9_status" character(1),
  "m9_level" character varying(4),
  "m10_value" double precision,
  "m10_status" character(1),
  "m11_value" double precision,
  "m11_status" character(1),
  "m12_value" double precision,
  "m12_status" character(1),
  "m12_level" character varying(4),
  "m13_value" double precision,
  "m13_status" character(1),
  "m13_level" character varying(4),
  "m14_value" double precision,
  "m14_status" character(1),
  "m15_value" double precision,
  "m15_status" character(1),
  "m16_value" double precision,
  "m16_status" character(1),
  "m17_value" double precision,
  "m17_status" character(1),
  "m18_value" double precision,
  "m18_status" character(1),
  "m19_value" double precision,
  "m19_status" character(1),
  "m20_value" double precision,
  "m20_status" character(1),
  "m21_value" double precision,
  "m21_status" character(1),
  "m22_value" double precision,
  "m22_status" character(1),
  "m23_value" double precision,
  "m23_status" character(1),
  "m24_value" double precision,
  "m24_status" character(1),
  "m25_value" double precision,
  "m25_status" character(1),
  "m26_value" double precision,
  "m26_status" character(1),
  "m27_value" double precision,
  "m27_status" character(1),
  "m28_value" double precision,
  "m28_status" character(1),
  "m29_value" double precision,
  "m29_status" character(1),
  "m30_value" double precision,
  "m30_status" character(1),
  "m31_value" double precision,
  "m31_status" character(1),
  "monitor_time" timestamp without time zone,
  "status" character(1),
  "water_quality_level" character varying(16),
  "record_type" character(1),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: id
--   station_id: 监测站id
--   m1_value: 水温监测值
--   m1_status: 监测结果：0 正常、1 超标
--   m1_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m2_value: PH监测值
--   m2_status: 监测结果：0 正常、1 超标
--   m2_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m3_value: 溶解氧监测值
--   m3_status: 监测结果：0 正常、2 偏低
--   m3_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m4_value: 浊度监测值
--   m4_status: 监测结果：0 正常、1 超标
--   m5_value: 电导率监测值
--   m5_status: 监测结果：0 正常、1 超标
--   m6_value: 氨氮监测值
--   m6_status: 监测结果：0 正常、1 超标
--   m6_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m7_value: 高锰酸盐指数监测值
--   m7_status: 监测结果：0 正常、1 超标
--   m7_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m8_value: 总磷监测值
--   m8_status: 监测结果：0 正常、1 超标
--   m8_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m9_value: 总氮监测值
--   m9_status: 监测结果：0 正常、1 超标
--   m9_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m10_value: 叶绿素a监测值
--   m10_status: 监测结果：0 正常、1 超标
--   m11_value: 藻密度监测值
--   m11_status: 监测结果：0 正常、1 超标
--   m12_value: 化学需氧量监测值
--   m12_status: 监测结果：0 正常、1 超标
--   m12_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m13_value: 五日生化需氧量监测值
--   m13_status: 监测结果：0 正常、1 超标
--   m13_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   m14_value: 监测值
--   m14_status: 监测结果：0 正常、1 超标
--   m15_value: 监测值
--   m15_status: 监测结果：0 正常、1 超标
--   m16_value: 监测值
--   m16_status: 监测结果：0 正常、1 超标
--   m17_value: 监测值
--   m17_status: 监测结果：0 正常、1 超标
--   m18_value: 监测值
--   m18_status: 监测结果：0 正常、1 超标
--   m19_value: 监测值
--   m19_status: 监测结果：0 正常、1 超标
--   m20_value: 监测值
--   m20_status: 监测结果：0 正常、1 超标
--   m21_value: 监测值
--   m21_status: 监测结果：0 正常、1 超标
--   m22_value: 监测值
--   m22_status: 监测结果：0 正常、1 超标
--   m23_value: 监测值
--   m23_status: 监测结果：0 正常、1 超标
--   m24_value: 监测值
--   m24_status: 监测结果：0 正常、1 超标
--   m25_value: 监测值
--   m25_status: 监测结果：0 正常、1 超标
--   m26_value: 监测值
--   m26_status: 监测结果：0 正常、1 超标
--   m27_value: 监测值
--   m27_status: 监测结果：0 正常、1 超标
--   m28_value: 监测值
--   m28_status: 监测结果：0 正常、1 超标
--   m29_value: 监测值
--   m29_status: 监测结果：0 正常、1 超标
--   m30_value: 监测值
--   m30_status: 监测结果：0 正常、1 超标
--   m31_value: 监测值
--   m31_status: 监测结果：0 正常、1 超标
--   monitor_time: 监测时间
--   status: 监测结果：0 正常、1 超标
--   water_quality_level: 水质级别：I、II、Ⅲ、IV、V、劣V
--   record_type: 记录类型：0 自动、1 手工
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

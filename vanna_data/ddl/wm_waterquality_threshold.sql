-- Table: public."wm_waterquality_threshold"
-- Table comment: 站点水质指标阈值
CREATE TABLE public."wm_waterquality_threshold" (
  "id" text NOT NULL,
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
  "m16_value" double precision,
  "m17_value" double precision,
  "m18_value" double precision,
  "m19_value" double precision,
  "m20_value" double precision,
  "m21_value" double precision,
  "m22_value" double precision,
  "m23_value" double precision,
  "m24_value" double precision,
  "m25_value" double precision,
  "m26_value" double precision,
  "m27_value" double precision,
  "m28_value" double precision,
  "m29_value" double precision,
  "m30_value" double precision,
  "m31_value" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: id
--   station_id: 监测站id
--   m1_value: 水温阈值(℃)
--   m2_value: pH阈值(无量纲)
--   m3_value: 溶解氧阈值(mg/L)
--   m4_value: 浊度阈值(NTU)
--   m5_value: 电导率阈值(μS/cm)
--   m6_value: 氨氮阈值(mg/L)
--   m7_value: 高锰酸盐指数阈值(mg/L)
--   m8_value: 总磷阈值(mg/L)
--   m9_value: 总氮阈值(mg/L)
--   m10_value: 叶绿素a阈值(ug/L)
--   m11_value: 藻密度阈值(cell/mL)
--   m12_value: 化学需氧量阈值(mg/L)
--   m13_value: 五日生化需氧量阈值(mg/L)
--   m14_value: 铜阈值(mg/L)
--   m15_value: 硒阈值(mg/L)
--   m16_value: 锌阈值(mg/L)
--   m17_value: 氟化物阈值(mg/L)
--   m18_value: 砷阈值(mg/L)
--   m19_value: 汞阈值(mg/L)
--   m20_value: 镉阈值(mg/L)
--   m21_value: 铬阈值(mg/L)
--   m22_value: 铅阈值(mg/L)
--   m23_value: 氰化物阈值(mg/L)
--   m24_value: 挥发酚阈值(mg/L)
--   m25_value: 石油类阈值(mg/L)
--   m26_value: 阴离子表面活性剂阈值(mg/L)
--   m27_value: 硫化物阈值(mg/L)
--   m28_value: 水中油阈值(mg/L)
--   m29_value: 硝酸盐阈值(mg/L)
--   m30_value: 生物毒性阈值(%)
--   m31_value: 大肠杆菌阈值(cell/L)
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

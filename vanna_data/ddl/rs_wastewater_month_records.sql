-- Table: public."rs_wastewater_month_records"
-- Table comment: 污染源监测月记录表
CREATE TABLE public."rs_wastewater_month_records" (
  "id" bigint,
  "timestamp" timestamp without time zone,
  "type" character varying(10),
  "pollutant_id" bigint,
  "status" character varying(10),
  "record_type" character varying(10),
  "monitor_year" integer,
  "monitor_month" integer,
  "remark" character varying(500),
  "ll" double precision,
  "ll_count" integer,
  "pfl" double precision,
  "pfl_count" integer,
  "m1_value" double precision,
  "m1_count" integer,
  "m2_value" double precision,
  "m2_count" integer,
  "m3_value" double precision,
  "m3_count" integer,
  "m4_value" double precision,
  "m4_count" integer,
  "m5_value" double precision,
  "m5_count" integer,
  "m6_value" double precision,
  "m6_count" integer,
  "m7_value" double precision,
  "m7_count" integer,
  "m8_value" double precision,
  "m8_count" integer,
  "m9_value" double precision,
  "m9_count" integer,
  "m10_value" double precision,
  "m10_count" integer,
  "m11_value" double precision,
  "m11_count" integer,
  "m12_value" double precision,
  "m12_count" integer,
  "m13_value" double precision,
  "m13_count" integer,
  "m14_value" double precision,
  "m14_count" integer,
  "m15_value" double precision,
  "m15_count" integer,
  "m16_value" double precision,
  "m16_count" integer,
  "m17_value" double precision,
  "m17_count" integer,
  "m18_value" double precision,
  "m18_count" integer,
  "m19_value" double precision,
  "m19_count" integer,
  "m20_value" double precision,
  "m20_count" integer,
  "m21_value" double precision,
  "m21_count" integer,
  "m22_value" double precision,
  "m22_count" integer,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(10)
);

-- Column comments:
--   id: 主键ID
--   timestamp: 统计月份起始时间（当月第一天00:00:00）
--   type: 类型：PS-排水口，PQ-排气口
--   pollutant_id: 排污口/排气口ID（关联
 rs_pollutant_info.id）
--   status: 当月综合状态：nobeyond-正常，below-偏低
 ，beyond-超标
--   record_type: 记录类型：0-正常统计，1-补录
--   monitor_year: 监测年份
--   monitor_month: 监测月份
--   remark: 备注
--   ll: 月流量（各日流量的平均值）
--   ll_count: 月流量有效数据计数（参与平均的天数）
--   pfl: 月排流量（各日排流量的累加值）
--   pfl_count: 月排流量有效数据计数（参与累加的天数）
--   m1_value: 【PS】化学需氧量(COD)月平均值 / 【PQ】烟尘
 月平均值
--   m1_count: m1 当月有效数据计数
--   m2_value: 【PS】总氮(TN)月平均值 / 【PQ】二氧化硫月平
 均值
--   m2_count: m2 当月有效数据计数
--   m3_value: 【PS】pH月平均值 / 【PQ】氮氧化物月平均值
--   m3_count: m3 当月有效数据计数
--   m4_value: 【PS】氨氮月平均值 / 【PQ】一氧化氮月平均值
--   m4_count: m4 当月有效数据计数
--   m5_value: 【PS】水温月平均值 / 【PQ】二氧化氮月平均值
--   m5_count: m5 当月有效数据计数
--   m6_value: 【PS】总磷月平均值 / 【PQ】一氧化碳月平均值
--   m6_count: m6 当月有效数据计数
--   m7_value: 【PS】悬浮物月平均值 / 【PQ】氯化氢月平均值
--   m7_count: m7 当月有效数据计数
--   m8_value: 【PS】余氯月平均值 / 【PQ】非甲烷总烃月平均
 值
--   m8_count: m8 当月有效数据计数
--   m9_value: 【PS】六价铬月平均值 / 【PQ】苯月平均值
--   m9_count: m9 当月有效数据计数
--   m10_value: 【PS】石油类月平均值 / 【PQ】甲苯月平均值
--   m10_count: m10 当月有效数据计数
--   m11_value: 【PS】氟化物月平均值 / 【PQ】二甲苯月平均
 值
--   m11_count: m11 当月有效数据计数
--   m12_value: 【PS】总铬月平均值 / 【PQ】碳氢化合物月平
 均值
--   m12_count: m12 当月有效数据计数
--   m13_value: 【PS】氰化物月平均值 / 【PQ】甲烷月平均值
--   m13_count: m13 当月有效数据计数
--   m14_value: 【PS】总锰月平均值 / 【PQ】氟化氢月平均值
--   m14_count: m14 当月有效数据计数
--   m15_value: 【PS】总银月平均值 / 【PQ】二氧化碳月平均
 值
--   m15_count: m15 当月有效数据计数
--   m16_value: 【PS】总铜月平均值 / 【PQ】1,3-二甲基苯月
 平均值
--   m16_count: m16 当月有效数据计数
--   m17_value: 【PS】总镍月平均值 / 【PQ】乙烯基苯(苯乙烯
 )月平均值
--   m17_count: m17 当月有效数据计数
--   m18_value: 【PS】总镉月平均值 / 【PQ】乙苯月平均值
--   m18_count: m18 当月有效数据计数
--   m19_value: 【PS】总砷月平均值 / 【PQ】1,2-二甲基苯月
 平均值
--   m19_count: m19 当月有效数据计数
--   m20_value: 【PS】总铅月平均值 / 【PQ】氨(NH3)月平均值
--   m20_count: m20 当月有效数据计数
--   m21_value: 【PS】浊度月平均值（仅排水口）
--   m21_count: m21 当月有效数据计数（仅排水口）
--   m22_value: 【PS】总锌月平均值（仅排水口）
--   m22_count: m22 当月有效数据计数（仅排水口）
--   create_by: 创建人ID
--   create_time: 创建时间
--   update_by: 更新人ID
--   update_time: 更新时间
--   del_flag: 删除标记：0-正常，1-删除

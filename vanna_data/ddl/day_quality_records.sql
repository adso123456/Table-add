-- Table: public."day_quality_records"
-- Table comment: 日质控数据
CREATE TABLE public."day_quality_records" (
  "id" bigint,
  "station_id" bigint,
  "type" character(1),
  "span_value5" double precision,
  "check_value5" double precision,
  "standard_value5" double precision,
  "monitor_time5" timestamp without time zone,
  "span_value6" double precision,
  "check_value6" double precision,
  "standard_value6" double precision,
  "monitor_time6" timestamp without time zone,
  "span_value7" double precision,
  "check_value7" double precision,
  "standard_value7" double precision,
  "monitor_time7" timestamp without time zone,
  "span_value8" double precision,
  "check_value8" double precision,
  "standard_value8" double precision,
  "monitor_time8" timestamp without time zone,
  "monitor_time" timestamp without time zone,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   station_id: 站点id
--   type: 类型：0 零点核查数据、1 跨度核查数据
--   span_value5: 氨氮仪器跨度值
--   check_value5: 氨氮零点/跨度核查数据
--   standard_value5: 氨氮标准样浓度
--   monitor_time5: 氨氮监测时间
--   span_value6: 高锰酸盐指数仪器跨度值
--   check_value6: 高锰酸盐指数零点/跨度核查数据
--   standard_value6: 高锰酸盐指数标准样浓度
--   monitor_time6: 高锰酸盐指数监测时间
--   span_value7: 总磷仪器跨度值
--   check_value7: 总磷零点/跨度核查数据
--   standard_value7: 总磷标准样浓度
--   monitor_time7: 总磷监测时间
--   span_value8: 总氮仪器跨度值
--   check_value8: 总氮零点/跨度核查数据
--   standard_value8: 总氮标准样浓度
--   monitor_time8: 总氮监测时间
--   monitor_time: 最新时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

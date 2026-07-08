-- Table: public."wh_hydrological_records_1"
-- Table comment: 水文数据表
CREATE TABLE public."wh_hydrological_records_1" (
  "id" bigint,
  "station_id" bigint,
  "indicator_code" character varying(100),
  "monitor_value" double precision,
  "monitor_time" timestamp without time zone,
  "record_type" character(1),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   station_id: 所属站点id
--   indicator_code: 监测指标编号
--   monitor_value: 监测值
--   monitor_time: 监测时间
--   record_type: 记录类型：0 自动、1 手工
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

-- Table: public."rs_warn_records"
-- Table comment: 污染预警消息通知
CREATE TABLE public."rs_warn_records" (
  "id" bigint,
  "station_id" bigint,
  "pollutant_id" bigint,
  "key_point_id" bigint,
  "warn_indicator" character varying(100),
  "warn_type" character(1),
  "warn_value" double precision,
  "standard_value" double precision,
  "unit" character varying(32),
  "water_quality_level" character varying(4),
  "warn_level" character(1),
  "warn_content" character varying(255),
  "warn_time" timestamp without time zone,
  "publish_status" character(1),
  "publish_time" timestamp without time zone,
  "check_status" character(1),
  "check_time" timestamp without time zone,
  "manual_auto" character(1),
  "release_status" character(1),
  "release_time" timestamp without time zone,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   station_id: 站点id，warn_type为0时
--   pollutant_id: 污染源id，warn_type为3时
--   key_point_id: 关键点id, warn_type为6时
--   warn_indicator: 预警指标
--   warn_type: 预警类型：0 水质预警、1 水文预警、2 气象预警、3 污染源预警、4 网络异常、5 仪器异常
--   warn_value: 预警值
--   standard_value: 标准值
--   unit: 单位
--   water_quality_level: 水质监测指标等级
--   warn_level: 告警等级：0 一般、1 严重、2 重度
--   warn_content: 预警内容
--   warn_time: 预警时间
--   publish_status: 是否发布：0 未发布、1 已发布
--   publish_time: 发布时间
--   check_status: 是否审核：0 未审核、1 已审核
--   check_time: 审核时间
--   manual_auto: 0 手动处理、1 自动处理
--   release_status: 是否解除：0 未解除、1 已解除
--   release_time: 解除时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

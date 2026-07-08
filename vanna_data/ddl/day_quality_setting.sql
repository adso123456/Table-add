-- Table: public."day_quality_setting"
-- Table comment: 日质控设置
CREATE TABLE public."day_quality_setting" (
  "id" bigint,
  "station_id" bigint,
  "indicator_code" character varying(100),
  "audit_by" bigint,
  "audit_time" timestamp without time zone,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   station_id: 站点id
--   indicator_code: 监测指标编号
--   audit_by: 审核人
--   audit_time: 审核时间
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

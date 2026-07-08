-- Table: public."min_value_setting"
-- Table comment: 最低检出限
CREATE TABLE public."min_value_setting" (
  "id" bigint,
  "indicator_code" character varying(100),
  "value" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   indicator_code: 监测指标编号
--   value: 最低检出限（mg/L）
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

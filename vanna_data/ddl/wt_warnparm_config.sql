-- Table: public."wt_warnparm_config"
-- Table comment: 监测预警参数配置表
CREATE TABLE public."wt_warnparm_config" (
  "id" bigint,
  "indicator_code" character varying(8),
  "l1_value" double precision,
  "l2_value" double precision,
  "l3_value" double precision,
  "l4_value" double precision,
  "l5_value" double precision,
  "zero" double precision,
  "zero_drift" double precision,
  "span" double precision,
  "span_drift" double precision,
  "compare" character(1),
  "type" character varying(4),
  "possible_value" double precision,
  "remove_warn_value" double precision,
  "frequency" bigint,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: id
--   indicator_code: 监测指标编号
--   l1_value: 一级
--   l2_value: 二级
--   l3_value: 三级
--   l4_value: 四级
--   l5_value: 五级
--   zero: 零点核查
--   zero_drift: 24小时零点漂移
--   span: 跨度核查
--   span_drift: 24小时跨度漂移
--   compare: 比较方式：0 无；1 ≤；2 ≥
--   type: 0 河流，1 湖泊
--   possible_value: 可能发生污染的告警值
--   remove_warn_value: 消除预警的参数值
--   frequency: 监测频率（小时计）
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

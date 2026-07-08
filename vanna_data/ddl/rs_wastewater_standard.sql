-- Table: public."rs_wastewater_standard"
-- Table comment: 废水/废气排放标准配置表
CREATE TABLE public."rs_wastewater_standard" (
  "id" bigint NOT NULL DEFAULT nextval('rs_wastewater_standard_1_id_seq'::regclass),
  "indicator_name" character varying(64),
  "apply_type" character(1),
  "l1_value" double precision,
  "l2_value" double precision,
  "l3_value" double precision,
  "max_value" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT '0'::bpchar,
  "jcdbh" character varying(64),
  "indicator_code" character varying(20),
  "type" character varying(10)
);

-- Column comments:
--   id: 主键id
--   indicator_name: 指标名称
--   apply_type: 适用类型：0 污水处理厂、1 其他
--   l1_value: 最低标准
--   l2_value: 小时标准
--   l3_value: 日标准
--   max_value: 最高允许排放浓度
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除
--   jcdbh: 监测点编号
--   indicator_code: 指标编码
--   type: 排放口类型：PS 排水口、PQ 排气口

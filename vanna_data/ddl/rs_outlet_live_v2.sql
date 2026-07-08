-- Table: public."rs_outlet_live_v2"
-- Table comment: 排污口实况
CREATE TABLE public."rs_outlet_live_v2" (
  "id" bigint,
  "outlet_id" bigint,
  "geom" geometry(Point,4326),
  "gate_morphology" character varying(100),
  "drainage_feature" character varying(100),
  "has_abnormal" character varying(10),
  "has_online_monitor" character varying(10),
  "has_sampling_condition" character varying(10),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "outlet_name" character varying(200)
);

-- Column comments:
--   id: 主键ID
--   outlet_id: 关联排污口ID
--   geom: 排污口所在位置
--   gate_morphology: 口门形态
--   drainage_feature: 排水特征
--   has_abnormal: 有无异常状况
--   has_online_monitor: 是否实现在线监测
--   has_sampling_condition: 是否具备采样条件
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   outlet_name: 排污口名称

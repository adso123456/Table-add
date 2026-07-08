-- Table: public."gis_ecologicalregion"
-- Table comment: 生态保护红线区域表
CREATE TABLE public."gis_ecologicalregion" (
  "id" bigint NOT NULL,
  "ecological_region_name" character varying(255),
  "ecological_region_code" character varying(32),
  "address" character varying(255),
  "geom" geometry(Geometry,4326),
  "population" bigint,
  "type" character(1),
  "service_target" character varying(255),
  "area" double precision,
  "ecosystem_vegetation" character varying(255),
  "human_activities" character varying(255),
  "environment_problems" character varying(255),
  "control_measures" character varying(255),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: 主键ID
--   ecological_region_name: 生态红线区域名称
--   ecological_region_code: 生态红线区域编码
--   address: 地址
--   geom: 空间几何数据
--   population: 人口数量
--   type: 类型
--   service_target: 生态服务目标
--   ecosystem_vegetation: 生态系统植被概况
--   human_activities: 人类活动影响描述
--   environment_problems: 生态环境问题描述
--   control_measures: 管控措施描述
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

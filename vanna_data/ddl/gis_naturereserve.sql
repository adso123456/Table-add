-- Table: public."gis_naturereserve"
-- Table comment: 自然保护区表
CREATE TABLE public."gis_naturereserve" (
  "id" bigint,
  "nature_reserve_name" character varying(255),
  "nature_reserve_code" character varying(32),
  "address" character varying(255),
  "geom" geometry(Geometry,4326),
  "department" character varying(100),
  "type" character(1),
  "level" character varying(8),
  "protect_target" character varying(255),
  "manage_org_name" character varying(100),
  "manage_org_type" character varying(8),
  "manage_org_level" character varying(8),
  "population" bigint,
  "first_protect_animals" character varying(255),
  "second_protect_animals" character varying(255),
  "first_protect_plants" character varying(255),
  "second_protect_plants" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   nature_reserve_name: 自然保护区名称
--   nature_reserve_code: 自然保护区编码
--   address: 地址
--   geom: 空间几何数据
--   department: 主管部门
--   type: 类型
--   level: 级别
--   protect_target: 主要保护对象
--   manage_org_name: 管理机构名称
--   manage_org_type: 管理机构类型
--   manage_org_level: 管理机构级别
--   population: 人口数量
--   first_protect_animals: 国家一级保护动物
--   second_protect_animals: 国家二级保护动物
--   first_protect_plants: 国家一级保护植物
--   second_protect_plants: 国家二级保护植物
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

-- Table: public."rs_outlet_info_v2"
-- Table comment: 排污口管理
CREATE TABLE public."rs_outlet_info_v2" (
  "id" bigint NOT NULL DEFAULT nextval('archive_outlet_id_seq'::regclass),
  "outlet_code_national" character varying(100),
  "outlet_code_local" character varying(100),
  "is_key_river_outlet" character varying(10),
  "key_river_name" character varying(200),
  "river_system" character varying(200),
  "province_city_district" character varying(200),
  "township" character varying(200),
  "outlet_name" character varying(200),
  "watershed_name" character varying(200),
  "outlet_category" character varying(100),
  "is_lake_inflow" character varying(10),
  "is_water_func_zone" character varying(10),
  "level1_water_func_zone" character varying(200),
  "level1_water_quality_target" character varying(50),
  "level2_water_func_zone" character varying(200),
  "level2_water_quality_target" character varying(50),
  "is_water_env_func_zone" character varying(10),
  "water_env_func_zone_name" character varying(200),
  "water_env_func_zone_target" character varying(50),
  "national_section_name" character varying(200),
  "provincial_section_name" character varying(200),
  "municipal_section_name" character varying(200),
  "river_chief_info" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1) DEFAULT '0'::character varying,
  "geom" geometry(Point,4326)
);

-- Column comments:
--   id: 主键ID
--   outlet_code_national: 排污口编码(国家统一赋码)
--   outlet_code_local: 排污口编码(省市系统自有编码)
--   is_key_river_outlet: 是否为重点河湖排污口
--   key_river_name: 重点河湖名称
--   river_system: 所属水系
--   province_city_district: 省市区县
--   township: 乡镇(街道)
--   outlet_name: 排污口名称
--   watershed_name: 流域名称
--   outlet_category: 排污口分类
--   is_lake_inflow: 是否为入湖河流
--   is_water_func_zone: 是否位于水功能区
--   level1_water_func_zone: 一级水功能区名称
--   level1_water_quality_target: 一级水功能区水质目标
--   level2_water_func_zone: 二级水功能区名称
--   level2_water_quality_target: 二级水功能区水质目标
--   is_water_env_func_zone: 是否位于水环境功能区
--   water_env_func_zone_name: 水环境功能区名称
--   water_env_func_zone_target: 水环境功能区目标
--   national_section_name: 国控断面名称
--   provincial_section_name: 省控断面名称
--   municipal_section_name: 市控断面名称
--   river_chief_info: 河长信息
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   geom: 图形信息

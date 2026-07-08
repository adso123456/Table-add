-- Table: public."wm_water_source_zone_v2"
-- Table comment: 饮用水水源地管理及监测-保护区
CREATE TABLE public."wm_water_source_zone_v2" (
  "id" bigint,
  "name" character varying(255),
  "city" character varying(100),
  "district" character varying(100),
  "township" character varying(100),
  "source_level" character varying(50),
  "zone_level" character varying(50),
  "area" numeric(15,4),
  "source_type" character varying(100),
  "source_status" character varying(100),
  "source_code" character varying(100),
  "remark" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "region_code" character varying(60),
  "geom" geometry(MultiPolygon,4326)
);

-- Column comments:
--   id: 主键ID
--   name: 名称
--   city: 地市
--   district: 区县
--   township: 乡镇
--   source_level: 水源地级别（县级以上；乡镇级；百吨千人）
--   zone_level: 保护区级别（1-一级保护区；2-二级保护区；3-准保护区）
--   area: 面积（单位：平方千米）
--   source_type: 水源地类型（河流型；湖库型；地下水型）
--   source_status: 水源地状态（在用；备用；应急；规划）
--   source_code: 水源地编码
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   region_code: 行政区代码
--   geom: 空间几何数据

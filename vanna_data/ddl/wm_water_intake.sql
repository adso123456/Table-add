-- Table: public."wm_water_intake"
-- Table comment: 水源地-取水口
CREATE TABLE public."wm_water_intake" (
  "id" bigint NOT NULL DEFAULT nextval('wm_water_intake_id_seq'::regclass),
  "geom" geometry(Point,4490),
  "region_code" character varying(50),
  "region_name" character varying(100),
  "name" character varying(100),
  "city" character varying(50),
  "county" character varying(50),
  "water_type" character varying(10),
  "used_mark" character varying(100),
  "township" character varying(100),
  "remark" character varying(254),
  "level" character varying(50),
  "code" character varying(100),
  "static_flag" character varying(12) DEFAULT '否'::character varying
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   region_code: 行政区编码
--   region_name: 行政区名称
--   name: 名称
--   city: 城市
--   county: 区县
--   water_type: 水源类型
--   used_mark: 使用状态
--   township: 乡镇
--   remark: 备注
--   level: 级别：乡镇、区县
--   code: 水源编码
--   static_flag: 统计标识：是、否

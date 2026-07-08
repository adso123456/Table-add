-- Table: public."wm_water_source_intake_v2"
-- Table comment: 饮用水水源地管理及监测-取水口
CREATE TABLE public."wm_water_source_intake_v2" (
  "id" bigint NOT NULL DEFAULT nextval('archive_water_source_intake_id_seq'::regclass),
  "name" character varying(255),
  "city" character varying(100),
  "district" character varying(100),
  "township" character varying(100),
  "source_level" character varying(50),
  "source_type" character varying(50),
  "source_status" character varying(50),
  "source_code" character varying(100),
  "water_quality_class" character varying(10),
  "supply_population" integer,
  "daily_supply_capacity" numeric(15,2),
  "annual_actual_withdrawal" numeric(15,4),
  "per_capita_withdrawal" numeric(10,2),
  "remark" text,
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1) DEFAULT '0'::character varying,
  "geom" geometry(Point,4326),
  "region_code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   name: 名称
--   city: 地市
--   district: 区县
--   township: 乡镇
--   source_level: 水源地级别（县级以上；乡镇级；百吨千人）
--   source_type: 水源地类型（河流型；湖库型；地下水型）
--   source_status: 水源地状态（在用；备用；应急；规划）
--   source_code: 水源地编码
--   water_quality_class: 水质类别（Ⅰ；Ⅱ；Ⅲ；Ⅳ；Ⅴ）
--   supply_population: 供水人口（人）
--   daily_supply_capacity: 日均供水能力（吨/天）
--   annual_actual_withdrawal: 年实际取水量（万吨）
--   per_capita_withdrawal: 人均取水量（升/天）
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   geom: 取水口位置
--   region_code: 行政区编码

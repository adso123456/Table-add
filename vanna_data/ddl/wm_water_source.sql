-- Table: public."wm_water_source"
-- Table comment: 水源地信息：通过code码关联
CREATE TABLE public."wm_water_source" (
  "id" bigint NOT NULL,
  "code" character varying(100),
  "name" character varying(100),
  "alias" character varying(100),
  "region_code" character varying(60),
  "region_name" character varying(100),
  "river_system_code" character varying(60),
  "river_system_name" character varying(100),
  "river_system_name_2" character varying(50),
  "river_system_name_3" character varying(100),
  "source_type" character varying(100),
  "source_state" character varying(100),
  "level" character varying(20),
  "protect_area_status" character varying(50),
  "protect_area_cert" character varying(100),
  "protect_level" smallint,
  "supply_type" character varying(60),
  "supply_service" character varying(100),
  "supply_water_daily" character varying(100),
  "supply_water_year" double precision,
  "supply_water_avg" double precision,
  "service_people_count" bigint,
  "water_word_info" character varying(100),
  "dbsqssw" real DEFAULT 0,
  "dbssjksw" real DEFAULT 0,
  "dxsmctj" character varying(50),
  "dxshsjzlx" character varying(50),
  "dxssjjs" real DEFAULT 0,
  "dxsswms" real DEFAULT 0,
  "ccsy" character varying(10) DEFAULT '否'::character varying,
  "cjjjdkhzb" character varying(10) DEFAULT '否'::character varying,
  "build_year" integer,
  "used_year" integer,
  "image_path" character varying(300),
  "remark" character varying(100),
  "geom" geometry(MultiPolygon,4326)
);

-- Column comments:
--   id: 主键ID
--   code: 代码
--   name: 水源名称
--   alias: 别名
--   region_code: 行政区代码
--   region_name: 行政区名称
--   river_system_code: 水系代码
--   river_system_name: 水系名称
--   river_system_name_2: 二级水系名称
--   river_system_name_3: 三级级水系名称
--   source_type: 水源类型
--   source_state: 水源状态
--   level: 级别
--   protect_area_status: 保护区划定情况
--   protect_area_cert: 保护区划定文号
--   protect_level: 保护区级别：1、2、3
--   supply_type: 供水类型
--   supply_service: 服务对象
--   supply_water_daily: 日均供水能力（吨/天）
--   supply_water_year: 年实际取水量(万吨)
--   supply_water_avg: 人均取水量（升/天）
--   service_people_count: 服务人数
--   water_word_info: 对应水厂名称
--   dbsqssw: 地表水取水水位（m）
--   dbssjksw: 地表水设计枯水位（m）
--   dxsmctj: 地下水埋藏条件
--   dxshsjzlx: 地下水含水介质类型
--   dxssjjs: 地下水设计降深（m）
--   dxsswms: 地下水水位埋深（m）
--   ccsy: 超采水源: 是、否
--   cjjjdkhzb: 长江经济带考核指标: 是、否
--   build_year: 取水口建成年份
--   used_year: 取水口正式使用年份
--   image_path: 图片路径
--   remark: 备注
--   geom: 空间几何数据

-- Table: public."se_watershed_river"
-- Table comment: 流域河流管理档案表
CREATE TABLE public."se_watershed_river" (
  "id" bigint NOT NULL DEFAULT nextval('se_watershed_river_id_seq'::regclass),
  "serial_no" integer,
  "river_name" character varying(100) DEFAULT NULL::character varying,
  "river_alias" character varying(500) DEFAULT NULL::character varying,
  "river_level" integer,
  "parent_river_name" character varying(100) DEFAULT NULL::character varying,
  "river_length" double precision,
  "hubei_length" double precision,
  "yichang_length" double precision,
  "watershed_area" double precision,
  "hubei_area" double precision,
  "yichang_area" double precision,
  "flow_districts" character varying(1000) DEFAULT NULL::character varying,
  "source_province" character varying(50) DEFAULT NULL::character varying,
  "source_county" character varying(100) DEFAULT NULL::character varying,
  "source_town" character varying(100) DEFAULT NULL::character varying,
  "source_village" character varying(300) DEFAULT NULL::character varying,
  "mouth_province" character varying(50) DEFAULT NULL::character varying,
  "mouth_county" character varying(100) DEFAULT NULL::character varying,
  "mouth_town" character varying(100) DEFAULT NULL::character varying,
  "mouth_village" character varying(300) DEFAULT NULL::character varying,
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character(1) DEFAULT '0'::bpchar
);

-- Column comments:
--   id: 主键id
--   serial_no: 序号
--   river_name: 河流名称
--   river_alias: 河流别称
--   river_level: 河流级别
--   parent_river_name: 上一级河流名称
--   river_length: 河流长度(km)
--   hubei_length: 湖北长度(km)
--   yichang_length: 宜昌长度(km)
--   watershed_area: 流域面积(km2)
--   hubei_area: 湖北面积(km2)
--   yichang_area: 宜昌面积(km2)
--   flow_districts: 流经市内行政区
--   source_province: 源头省
--   source_county: 源头县（市）
--   source_town: 源头乡镇
--   source_village: 源头村
--   mouth_province: 河口省
--   mouth_county: 河口县（市）
--   mouth_town: 河口乡镇
--   mouth_village: 河口村
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除、1-已删除

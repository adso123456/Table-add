-- Table: public."gis_headwaters"
-- Table comment: 水源地表
CREATE TABLE public."gis_headwaters" (
  "id" bigint NOT NULL,
  "headwaters_name" character varying(255),
  "headwaters_code" character varying(32),
  "address" character varying(255),
  "geom" geometry(Geometry,4326),
  "level" character varying(8),
  "type" character(1),
  "water_intake_quantity" double precision,
  "water_supply_population" bigint,
  "is_protect_region" character(1),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: 主键ID
--   headwaters_name: 水源地名称
--   headwaters_code: 水源地编码
--   address: 地址
--   geom: 空间几何数据
--   level: 级别
--   type: 类型
--   water_intake_quantity: 年取水量
--   water_supply_population: 供水人口数
--   is_protect_region: 是否在保护区范围内
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

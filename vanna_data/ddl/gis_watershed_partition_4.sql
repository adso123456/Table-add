-- Table: public."gis_watershed_partition_4"
-- Table comment: 四级流域分区表
CREATE TABLE public."gis_watershed_partition_4" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "basin" character varying(50),
  "last_name" character varying(50),
  "poly_area" double precision,
  "name" character varying(50),
  "area" double precision,
  "section_name" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   basin: 流域
--   last_name: 上一级流域名称
--   poly_area: 多边形面积
--   name: 名称
--   area: 面积：平方米
--   section_name: 对应断面名称

-- Table: public."gis_watershed_partition_3"
-- Table comment: 三级流域分区表
CREATE TABLE public."gis_watershed_partition_3" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "basin" character varying(50),
  "name" character varying(50),
  "area" double precision
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   basin: 流域
--   name: 名称
--   area: 面积：平方米

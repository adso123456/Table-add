-- Table: public."layer_partition_2"
-- Table comment: 二级分区
CREATE TABLE public."layer_partition_2" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "name" character varying(50),
  "name_1" character varying(50),
  "area" double precision
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   name: 分区名称
--   name_1: 一级分区名称
--   area: 面积

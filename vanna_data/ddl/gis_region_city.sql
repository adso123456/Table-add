-- Table: public."gis_region_city"
-- Table comment: 城市行政区划表
CREATE TABLE public."gis_region_city" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "region_name" character varying(50),
  "region_code" character varying(20)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   region_name: 行政区划名称
--   region_code: 行政区划编码

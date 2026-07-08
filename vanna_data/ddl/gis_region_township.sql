-- Table: public."gis_region_township"
-- Table comment: 行政区划-乡镇
CREATE TABLE public."gis_region_township" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "region_code" character varying(20),
  "county" character varying(60),
  "region_name" character varying(50),
  "city" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   region_code: 行政区划编码
--   county: 区县名称
--   region_name: 行政区划名称
--   city: 市级名称

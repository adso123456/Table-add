-- Table: public."gis_region_county"
-- Table comment: 行政区-区县
CREATE TABLE public."gis_region_county" (
  "id" integer NOT NULL DEFAULT nextval('gis_region_qx_id_seq'::regclass),
  "geom" geometry(MultiPolygon,4326),
  "region_name" character varying(60),
  "city" character varying(50),
  "region_code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   region_name: 行政区名称
--   city: 市级名称
--   region_code: 行政区编码

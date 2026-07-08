-- Table: public."layer_industrial_ghysgw"
-- Table comment: 工业园区-规划雨水管网
CREATE TABLE public."layer_industrial_ghysgw" (
  "id" integer,
  "geom" geometry(MultiLineString,4326),
  "name" character varying(10),
  "code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   name: 名称
--   code: 编码

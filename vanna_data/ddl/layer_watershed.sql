-- Table: public."layer_watershed"
-- Table comment: 工业园区-汇水区
CREATE TABLE public."layer_watershed" (
  "id" integer,
  "name" character varying,
  "code" character varying,
  "geom" geometry(MultiLineString,4326)
);

-- Column comments:
--   id: 主键ID
--   name: 名称
--   code: 编码
--   geom: 空间几何数据

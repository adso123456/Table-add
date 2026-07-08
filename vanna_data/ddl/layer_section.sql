-- Table: public."layer_section"
-- Table comment: 工业园区-监测断面
CREATE TABLE public."layer_section" (
  "id" integer,
  "x" double precision,
  "y" double precision,
  "name" character varying,
  "code" character varying,
  "geom" geometry(Point,4326)
);

-- Column comments:
--   id: 主键ID
--   x: X坐标
--   y: Y坐标
--   name: 名称
--   code: 编码
--   geom: 空间几何数据

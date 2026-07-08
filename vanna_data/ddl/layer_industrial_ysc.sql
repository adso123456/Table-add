-- Table: public."layer_industrial_ysc"
-- Table comment: 工业园区-雨水池
CREATE TABLE public."layer_industrial_ysc" (
  "id" integer NOT NULL,
  "geom" geometry(Point,4326),
  "x" double precision,
  "y" double precision,
  "name" character varying(10),
  "code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   x: X坐标
--   y: Y坐标
--   name: 名称
--   code: 编码

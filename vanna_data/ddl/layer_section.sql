-- Table: public."layer_section"
-- Table comment: 工业园区-监测断面
CREATE TABLE public."layer_section" (
  "id" integer NOT NULL DEFAULT nextval('"监测断面_id_seq"'::regclass),
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

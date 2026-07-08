-- Table: public."layer_industrial_lsf"
-- Table comment: 工业园区-园区临时闸阀
CREATE TABLE public."layer_industrial_lsf" (
  "id" integer NOT NULL,
  "geom" geometry(Point,4326),
  "name" character varying(10),
  "code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   name: 名称
--   code: 编码

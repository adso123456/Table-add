-- Table: public."layer_industrial_yjf"
-- Table comment: 工业园区-园区永久闸阀
CREATE TABLE public."layer_industrial_yjf" (
  "id" integer,
  "geom" geometry(Point,4326),
  "name" character varying(10),
  "code" character varying(50)
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   name: 名称
--   code: 编码

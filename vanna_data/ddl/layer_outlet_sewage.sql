-- Table: public."layer_outlet_sewage"
-- Table comment: 工业园区-污水排放口
CREATE TABLE public."layer_outlet_sewage" (
  "id" integer NOT NULL DEFAULT nextval('"污水排放口_id_seq"'::regclass),
  "x" double precision,
  "y" double precision,
  "name" character varying,
  "code" character varying,
  "jcdbh" character varying,
  "geom" geometry(Point,4326)
);

-- Column comments:
--   id: 主键ID
--   x: X坐标
--   y: Y坐标
--   name: 名称
--   code: 编码
--   jcdbh: 监测点编号
--   geom: 空间几何数据

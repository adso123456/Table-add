-- Table: public."layer_boundary_enterprise"
-- Table comment: 工业园区-企业边界
CREATE TABLE public."layer_boundary_enterprise" (
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

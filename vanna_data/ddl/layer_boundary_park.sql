-- Table: public."layer_boundary_park"
-- Table comment: 工业园区-园区边界
CREATE TABLE public."layer_boundary_park" (
  "id" integer NOT NULL,
  "geom" geometry(MultiPolygon,4326),
  "name" character varying(28),
  "code" character varying(50),
  "name_part" character varying(255),
  "region_name" character varying(100),
  "park_level" integer
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   name: 名称
--   code: 编码
--   name_part: 分园名称
--   region_name: 行政区名称
--   park_level: 园区级别：0-未知、1-国家级、2-省级、3-市级

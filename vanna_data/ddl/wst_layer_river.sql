-- Table: public."wst_layer_river"
-- Table comment: 溯源图层河流表
CREATE TABLE public."wst_layer_river" (
  "id" bigint,
  "river_code" character varying(128),
  "river_name" character varying(255),
  "next_down" bigint,
  "river_class" character varying(64),
  "length_km" numeric,
  "from_z" numeric,
  "to_z" numeric,
  "geom" geometry(MultiLineString,4326),
  "created_at" timestamp without time zone,
  "updated_at" timestamp without time zone
);

-- Column comments:
--   id: 主键ID
--   river_code: 河流编码
--   river_name: 河流名称
--   next_down: 下游河流ID
--   river_class: 河流类别
--   length_km: 河流长度（公里）
--   from_z: 起点高程
--   to_z: 终点高程
--   geom: 空间几何数据
--   created_at: 创建时间
--   updated_at: 更新时间

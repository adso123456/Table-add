-- Table: public."wm_panorama_layer"
-- Table comment: 全景图层信息表
CREATE TABLE public."wm_panorama_layer" (
  "id" bigint,
  "point_name" character varying(255),
  "topic" character varying(255),
  "directory_id" bigint,
  "longitude" numeric(20,10),
  "latitude" numeric(20,10),
  "icon" character varying(500),
  "coverage_radius" numeric(10,2),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "is_deleted" boolean
);

-- Column comments:
--   id: 自增主键
--   point_name: 点位名称
--   topic: 所属专题
--   directory_id: 目录ID
--   longitude: 经度
--   latitude: 纬度
--   icon: 图标地址
--   coverage_radius: 覆盖半径(km)
--   create_time: 创建时间
--   update_time: 更新时间
--   is_deleted: 是否删除（true:已删除，false:未删除）

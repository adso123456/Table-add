-- Table: public."wm_panorama_video"
-- Table comment: 全景视频信息表
CREATE TABLE public."wm_panorama_video" (
  "id" integer,
  "layer_id" integer,
  "name" character varying(255),
  "shoot_time" timestamp without time zone,
  "description" text,
  "url" character varying(500),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "is_deleted" boolean
);

-- Column comments:
--   id: 自增主键
--   layer_id: 所属全景图层ID
--   name: 视频名称
--   shoot_time: 拍摄时间
--   description: 描述
--   url: 访问地址
--   create_time: 创建时间
--   update_time: 更新时间
--   is_deleted: 是否删除（true:已删除，false:未删除）

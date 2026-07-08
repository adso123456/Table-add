-- Table: public."wm_panorama_layer_relation"
-- Table comment: 全景图层关联关系表
CREATE TABLE public."wm_panorama_layer_relation" (
  "id" bigint NOT NULL DEFAULT nextval('wm_panorama_layer_relation_id_seq'::regclass),
  "panorama_id" bigint,
  "layer_id" character varying(255),
  "feature_id" character varying(255),
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" boolean DEFAULT false
);

-- Column comments:
--   id: 自增主键
--   panorama_id: 全景ID
--   layer_id: 图层ID
--   feature_id: 要素ID
--   create_time: 创建时间
--   update_time: 更新时间
--   is_deleted: 是否删除（true:已删除，false:未删除）

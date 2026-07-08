-- Table: public."wm_raster_inversion_config"
-- Table comment: 遥感反演配置表
CREATE TABLE public."wm_raster_inversion_config" (
  "id" bigint NOT NULL,
  "type_code" bigint NOT NULL,
  "name" character varying(100) NOT NULL,
  "boundaries_json" text NOT NULL,
  "labels_json" text NOT NULL,
  "colors_json" text NOT NULL,
  "create_time" timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "update_time" timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character(1) NOT NULL DEFAULT 0
);

-- Column comments:
--   id: 主键ID
--   type_code: 反演类型编码
--   name: 名称
--   create_time: 创建时间
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

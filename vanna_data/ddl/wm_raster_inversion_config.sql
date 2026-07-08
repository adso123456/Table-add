-- Table: public."wm_raster_inversion_config"
-- Table comment: 遥感反演配置表
CREATE TABLE public."wm_raster_inversion_config" (
  "id" bigint,
  "type_code" bigint,
  "name" character varying(100),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   type_code: 反演类型编码
--   name: 名称
--   create_time: 创建时间
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

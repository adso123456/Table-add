-- Table: public."wm_raster_info"
-- Table comment: 遥感影像栅格信息表
CREATE TABLE public."wm_raster_info" (
  "id" bigint,
  "scene_id" character varying(200),
  "satellite_info" character varying(100),
  "sensor_info" character varying(100),
  "orbit_name" character varying(50),
  "processing_version" character varying(100),
  "content_type" character varying(50),
  "data_location" character varying(100),
  "image_datetime" timestamp without time zone,
  "image_path" character varying(500),
  "inversion_flag" character varying(1),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   scene_id: 遥感监测影像信息实体类
--   satellite_info: 拍摄卫星
--   sensor_info: 传感器信息
--   orbit_name: 轨道名称
--   processing_version: 数据级别
--   content_type: 文件内容类型
--   data_location: 数据位置
--   image_datetime: 影像获取时间（年_月_日_时_分）
--   image_path: 缩略图路径
--   inversion_flag: 是否反演
--   create_time: 创建时间
--   update_time: 更新时间
--   del_flag: 删除标志：0-正常，1-已删除

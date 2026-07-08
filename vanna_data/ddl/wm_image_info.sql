-- Table: public."wm_image_info"
-- Table comment: 档案图片信息表：用于保存各种站点、断面、污染源的图片信息
CREATE TABLE public."wm_image_info" (
  "id" bigint,
  "pid" bigint,
  "image_url" character varying(255),
  "image_formats" character varying(15),
  "image_type" smallint,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "image_name" character varying(255),
  "image_tag" character varying(100)
);

-- Column comments:
--   id: 主键ID
--   pid: 照片关联的id
--   image_url: 图片地址
--   image_formats: 图片格式
--   image_type: 图片类型：0-未知、1-断面、2-自动站......
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除、1-已删除
--   image_name: 文件名称：原始文件名
--   image_tag: 图片标签

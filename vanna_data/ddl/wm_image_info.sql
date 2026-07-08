-- Table: public."wm_image_info"
-- Table comment: 档案图片信息表：用于保存各种站点、断面、污染源的图片信息
CREATE TABLE public."wm_image_info" (
  "id" bigint NOT NULL,
  "pid" bigint NOT NULL,
  "image_url" character varying(255) NOT NULL,
  "image_formats" character varying(15),
  "image_type" smallint DEFAULT 0,
  "create_by" bigint DEFAULT 1,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint DEFAULT 1,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character(1) DEFAULT '0'::bpchar,
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

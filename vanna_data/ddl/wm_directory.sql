-- Table: public."wm_directory"
-- Table comment: 目录树实体
CREATE TABLE public."wm_directory" (
  "id" bigint,
  "name" character varying(255),
  "parent_id" bigint,
  "path" character varying(1024),
  "description" character varying(512),
  "sort" integer,
  "type" character varying(32),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "is_deleted" boolean
);

-- Column comments:
--   id: 主键ID
--   name: 目录名称
--   parent_id: 父目录ID，根目录为null
--   path: 完整路径
--   description: 目录描述
--   sort: 排序值
--   type: 目录类型（如：panorama/other）
--   create_time: 创建时间
--   update_time: 更新时间
--   is_deleted: 是否删除

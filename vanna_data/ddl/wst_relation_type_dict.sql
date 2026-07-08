-- Table: public."wst_relation_type_dict"
-- Table comment: 关系大类字典表，用于维护资产关系的大类编码
CREATE TABLE public."wst_relation_type_dict" (
  "id" bigint,
  "type_code" character varying(100),
  "type_name" character varying(100),
  "description" character varying(500),
  "sort_order" integer,
  "status" character varying(50),
  "created_at" timestamp without time zone,
  "updated_at" timestamp without time zone
);

-- Column comments:
--   id: 主键ID
--   type_code: 关系大类编码，例如 ownership、discharge、monitoring
--   type_name: 关系大类名称
--   description: 关系大类说明
--   sort_order: 排序号
--   status: 状态，active 表示启用
--   created_at: 创建时间
--   updated_at: 更新时间

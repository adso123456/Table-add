-- Table: public."metadata_view"
-- Table comment: 元数据-视图
CREATE TABLE public."metadata_view" (
  "code" character varying(255),
  "parent_id" character varying(255),
  "name" character varying(255),
  "aliasname" character varying(255),
  "type" character varying(255),
  "LayerName" character varying(255),
  "LayerType" character varying(255),
  "create_date" timestamp without time zone,
  "table_name" character varying(21) NOT NULL DEFAULT ''::character varying
);

-- Column comments:
--   code: 编码
--   parent_id: 父级ID
--   name: 关键字或文件名(不含后缀)
--   aliasname: 别名
--   type: 类型
--   LayerName: 图层名称
--   LayerType: 图层类型
--   create_date: 创建时间
--   table_name: 表名

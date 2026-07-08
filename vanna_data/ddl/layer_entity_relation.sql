-- Table: public."layer_entity_relation"
-- Table comment: 图层-要素关联关系表
CREATE TABLE public."layer_entity_relation" (
  "id" bigint,
  "entity_code_1" character varying(100),
  "layer_name_1" character varying(100),
  "relation" character varying(50),
  "entity_code_2" character varying(100),
  "layer_name_2" character varying(100),
  "create_date" timestamp without time zone,
  "delete_mark" smallint
);

-- Column comments:
--   id: 主键
--   entity_code_1: 要素编码1
--   layer_name_1: 图层名称1
--   relation: 关系名称
--   entity_code_2: 要素编码2
--   layer_name_2: 图层名称2
--   create_date: 创建时间
--   delete_mark: 删除标志：0-正常、1-删除

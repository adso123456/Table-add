-- Table: public."layer_entity_process"
-- Table comment: 溯源关系查询流程：使用到的图层信息
CREATE TABLE public."layer_entity_process" (
  "id" bigint,
  "process_type" character varying(100),
  "layer_type" smallint,
  "layer_name_en" character varying(100),
  "layer_name_cn" character varying(150),
  "geom_type" character varying(50),
  "layer_level" smallint,
  "query_expand_mark" smallint,
  "remark" character varying(255)
);

-- Column comments:
--   id: 主键
--   process_type: 溯源查询类型：industrial-工业园区
--   layer_type: 溯源查询类型：0-查询图层、1-静态图层...
--   layer_name_en: 图层英文名称
--   layer_name_cn: 图层中文名称
--   geom_type: 图形类型：点、线、面
--   layer_level: 图层层级：查询过程的级别
--   query_expand_mark: 扩展查询标记：关联查询相关属性
--   remark: 备注

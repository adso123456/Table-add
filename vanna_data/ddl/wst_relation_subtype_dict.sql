-- Table: public."wst_relation_subtype_dict"
-- Table comment: 关系子类字典表，维护具体业务关系类型、标准方向和允许资产类型
CREATE TABLE public."wst_relation_subtype_dict" (
  "id" bigint NOT NULL DEFAULT nextval('wst_relation_subtype_dict_id_seq'::regclass),
  "relation_type" character varying(100) NOT NULL,
  "relation_subtype" character varying(100) NOT NULL,
  "relation_name" character varying(100) NOT NULL,
  "source_type_codes" character varying(500) NOT NULL,
  "target_type_codes" character varying(500) NOT NULL,
  "source_label" character varying(100),
  "target_label" character varying(100),
  "direction_desc" character varying(200),
  "allow_manual" boolean DEFAULT true,
  "allow_import" boolean DEFAULT true,
  "allow_graph_edit" boolean DEFAULT true,
  "allow_map_draw" boolean DEFAULT true,
  "default_confidence" numeric(5,2) DEFAULT 1.00,
  "sort_order" integer DEFAULT 0,
  "status" character varying(50) DEFAULT 'active'::character varying,
  "description" character varying(500),
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_at" timestamp without time zone DEFAULT now()
);

-- Column comments:
--   id: 主键ID
--   relation_type: 关系大类编码，对应 wst_relation_type_dict.type_code
--   relation_subtype: 关系子类编码，例如 enterprise_outfall
--   relation_name: 关系子类中文名称，例如 企业关联排污口
--   source_type_codes: 允许作为源对象的资产类型，多个用英文逗号分隔
--   target_type_codes: 允许作为目标对象的资产类型，多个用英文逗号分隔
--   source_label: 源对象中文标签
--   target_label: 目标对象中文标签
--   direction_desc: 标准方向说明，例如 企业 → 排污口
--   allow_manual: 是否允许人工录入
--   allow_import: 是否允许导入
--   allow_graph_edit: 是否允许图谱编辑
--   allow_map_draw: 是否允许地图连线绘制
--   default_confidence: 默认置信度
--   sort_order: 排序号
--   status: 状态，active 表示启用
--   description: 关系子类说明
--   created_at: 创建时间
--   updated_at: 更新时间

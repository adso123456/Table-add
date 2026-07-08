-- Table: public."wst_asset_relation"
-- Table comment: 资产关系实例表，存储资产与资产之间的一度业务关系，不代表水流路径
CREATE TABLE public."wst_asset_relation" (
  "id" bigint NOT NULL DEFAULT nextval('wst_asset_relation_id_seq'::regclass),
  "source_asset_id" bigint NOT NULL,
  "target_asset_id" bigint NOT NULL,
  "relation_type" character varying(100) NOT NULL,
  "relation_subtype" character varying(100) NOT NULL,
  "source_type" character varying(50),
  "confidence" numeric(5,2),
  "status" character varying(50) DEFAULT 'confirmed'::character varying,
  "metadata_json" jsonb,
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_at" timestamp without time zone DEFAULT now()
);

-- Column comments:
--   id: 主键ID
--   source_asset_id: 源资产ID，对应 wst_asset.id
--   target_asset_id: 目标资产ID，对应 wst_asset.id
--   relation_type: 关系大类编码，对应 wst_relation_type_dict.type_code
--   relation_subtype: 关系子类编码，对应 wst_relation_subtype_dict.relation_subtype
--   source_type: 关系来源，可选 manual、import、spatial、system
--   confidence: 置信度
--   status: 状态，可选 confirmed、candidate、disabled
--   metadata_json: 扩展信息，例如备注、导入来源、原始字段等
--   created_at: 创建时间
--   updated_at: 更新时间

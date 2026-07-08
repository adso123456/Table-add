-- Table: public."wst_asset_type_dict"
-- Table comment: 水安全溯源模块-资产类型字典表，用于统一管理资产类型、图层、图标、几何类型和前端展示规则
CREATE TABLE public."wst_asset_type_dict" (
  "id" bigint NOT NULL DEFAULT nextval('wst_asset_type_dict_id_seq'::regclass),
  "asset_type" character varying(100) NOT NULL,
  "asset_type_name" character varying(200) NOT NULL,
  "parent_type" character varying(100),
  "category" character varying(100),
  "geometry_type" character varying(50),
  "icon_name" character varying(100),
  "layer_name" character varying(100),
  "default_visible" boolean DEFAULT true,
  "sort_no" integer DEFAULT 0,
  "status" character varying(50) DEFAULT 'active'::character varying,
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone DEFAULT now(),
  "del_flag" smallint DEFAULT 0,
  "asset_group" character varying(100),
  "asset_group_name" character varying(100),
  "group_sort" integer,
  "group_description" text
);

-- Column comments:
--   id: 主键ID
--   asset_type: 资产类型编码，例如 national_section、auto_station、outfall、water_enterprise、chemical_park、camera
--   asset_type_name: 资产类型名称，例如国控断面、自动站、排污口、涉水企业、化工园区、摄像头
--   parent_type: 上级资产类型编码，用于资产类型分组
--   category: 资产分类，例如 monitoring=监测类，pollution=污染源类，supervision=监管类，emergency=应急类，network=网络类
--   geometry_type: 默认几何类型：Point、LineString、Polygon、Geometry
--   icon_name: 前端图标名称
--   layer_name: 前端图层名称
--   default_visible: 地图上是否默认显示
--   sort_no: 排序号
--   status: 状态：active=启用，disabled=停用
--   metadata_json: 扩展属性JSON
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除
--   asset_group: 资产分组编码
--   asset_group_name: 资产分组名称
--   group_sort: 分组排序号
--   group_description: 分组描述

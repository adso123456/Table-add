-- Table: public."wst_trace_node"
-- Table comment: 水安全溯源模块-溯源拓扑节点表，用于存储河网、管网、园区排污河流、排口挂接点、断面挂接点、园区出口等 pgRouting 节点
CREATE TABLE public."wst_trace_node" (
  "id" bigint,
  "node_code" character varying(100),
  "node_name" character varying(200),
  "node_type" character varying(100),
  "network_type" character varying(100),
  "zone_id" bigint,
  "is_boundary_node" boolean,
  "boundary_type" character varying(100),
  "boundary_name" character varying(200),
  "source_asset_id" bigint,
  "source_system" character varying(100),
  "source_id" character varying(200),
  "longitude" numeric(12,8),
  "latitude" numeric(12,8),
  "elevation" numeric(12,3),
  "status" character varying(50),
  "geom" geometry(Point,4326),
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone,
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone,
  "del_flag" smallint,
  "asset_id" bigint
);

-- Column comments:
--   id: 主键ID，同时作为 pgRouting 的 source/target 节点ID
--   node_code: 节点编码
--   node_name: 节点名称
--   node_type: 节点类型，例如 river_node、pipe_node、outfall_snap_node、section_snap_node、intake_snap_node、gate_node、park_outlet_node
--   network_type: 网络类型，例如 river=外部河网，park_pipe=园区管网，park_river=园区内部排污河流，mixed=混合衔接网络
--   zone_id: 所属分区ID，关联 wst_control_zone.id
--   is_boundary_node: 是否边界节点，例如园区出口、管网入河口、内外网络衔接点
--   boundary_type: 边界节点类型，例如 park_outlet、pipe_to_river、river_inlet、external_river_join
--   boundary_name: 边界节点名称
--   source_asset_id: 来源资产ID，如果该节点由某个资产生成，可关联 wst_asset.id
--   source_system: 数据来源系统
--   source_id: 来源系统中的原始ID
--   longitude: 经度
--   latitude: 纬度
--   elevation: 高程，单位米
--   status: 状态：active=启用，disabled=停用，candidate=候选，invalid=无效
--   geom: 节点点几何，坐标系SRID=4326
--   metadata_json: 扩展属性JSON
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除
--   asset_id: 资产ID

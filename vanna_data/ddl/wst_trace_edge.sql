-- Table: public."wst_trace_edge"
-- Table comment: 水安全溯源模块-溯源拓扑边表，用于存储河网、管网、排水路径、园区内外衔接路径，是 pgRouting 上下游分析的核心边表
CREATE TABLE public."wst_trace_edge" (
  "id" bigint NOT NULL DEFAULT nextval('wst_trace_edge_id_seq'::regclass),
  "edge_code" character varying(100),
  "edge_name" character varying(200),
  "source" bigint NOT NULL,
  "target" bigint NOT NULL,
  "edge_type" character varying(100) NOT NULL,
  "network_type" character varying(100) NOT NULL,
  "from_network" character varying(100),
  "to_network" character varying(100),
  "zone_id" bigint,
  "river_name" character varying(200),
  "river_code" character varying(100),
  "pipe_code" character varying(100),
  "cost" numeric(18,3) NOT NULL,
  "reverse_cost" numeric(18,3) DEFAULT '-1'::integer,
  "length_m" numeric(18,3),
  "flow_direction" character varying(50) DEFAULT 'source_to_target'::character varying,
  "flow_mode" character varying(100) DEFAULT 'normal'::character varying,
  "control_mode" character varying(100),
  "gate_asset_id" bigint,
  "pump_asset_id" bigint,
  "is_split_edge" boolean DEFAULT false,
  "original_edge_id" bigint,
  "status" character varying(50) DEFAULT 'active'::character varying,
  "geom" geometry(LineString,4326) NOT NULL,
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone DEFAULT now(),
  "del_flag" smallint DEFAULT 0,
  "source_asset_id" bigint,
  "from_node_id" bigint,
  "to_node_id" bigint,
  "direction_status" character varying(64)
);

-- Column comments:
--   id: 主键ID，同时作为 pgRouting 的边ID
--   edge_code: 边编码
--   edge_name: 边名称
--   source: 起点拓扑节点ID，关联 wst_trace_node.id，约定为默认水流方向的上游节点
--   target: 终点拓扑节点ID，关联 wst_trace_node.id，约定为默认水流方向的下游节点
--   edge_type: 边类型，例如 river=河道，pipe=管线，park_pipe=园区管网，park_river=园区内部排污河流，discharge=排放连接边，boundary=边界衔接边
--   network_type: 网络类型，例如 river=外部河网，park_pipe=园区管网，park_river=园区内部排污河流，mixed=混合衔接网络
--   from_network: 起点所属网络类型，用于表达园区管网到园区河流、园区河流到外部河网的衔接
--   to_network: 终点所属网络类型，用于表达网络转换关系
--   zone_id: 所属分区ID，关联 wst_control_zone.id
--   river_name: 河流名称
--   river_code: 河流编码
--   pipe_code: 管线编码
--   cost: 正向通行成本，通常为长度米；source->target 可通行时为正数，不可通行时为-1
--   reverse_cost: 反向通行成本；普通单向水流通常为-1，库区/回水/双向场景可设置为正数
--   length_m: 边长度，单位米
--   flow_direction: 流向说明，默认 source_to_target 表示 source 到 target 为水流方向
--   flow_mode: 流向模式：normal=正常单向，bidirectional=双向，controlled=受控，reservoir=库区/回水，unknown=未知
--   control_mode: 控制方式，例如 gate=闸门，pump=泵站，manual=人工控制，temporary_dam=临时筑坝
--   gate_asset_id: 关联闸门/闸坝资产ID，关联 wst_asset.id
--   pump_asset_id: 关联泵站资产ID，关联 wst_asset.id
--   is_split_edge: 是否由原始边拆分生成
--   original_edge_id: 原始边ID，资产挂接到边中间并拆边时记录来源边
--   status: 状态：active=启用，disabled=停用，split=已拆分，invalid=无效
--   geom: 边线几何，坐标系SRID=4326
--   metadata_json: 扩展属性JSON，用于存储管径、材质、坡度、流速、原始河段编码等扩展信息
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除
--   source_asset_id: 源资产ID
--   from_node_id: 上游节点ID
--   to_node_id: 下游节点ID
--   direction_status: 流向状态

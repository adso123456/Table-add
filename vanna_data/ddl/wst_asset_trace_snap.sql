-- Table: public."wst_asset_trace_snap"
-- Table comment: 水安全溯源模块-资产拓扑挂接表，用于维护业务资产与溯源拓扑节点之间的挂接关系，是资产进入 pgRouting 网络计算的桥梁
CREATE TABLE public."wst_asset_trace_snap" (
  "id" bigint,
  "asset_id" bigint,
  "trace_node_id" bigint,
  "trace_edge_id" bigint,
  "snap_point_geom" geometry(Point,4326),
  "asset_point_geom" geometry(Point,4326),
  "distance_m" numeric(18,3),
  "snap_type" character varying(100),
  "snap_role" character varying(100),
  "snap_method" character varying(100),
  "snap_status" character varying(50),
  "is_primary" boolean,
  "confidence" numeric(5,2),
  "confirmed_by" character varying(100),
  "confirmed_at" timestamp without time zone,
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone,
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone,
  "del_flag" smallint,
  "snap_node_id" bigint,
  "snap_edge_id" bigint,
  "snap_distance_m" numeric(18,3),
  "network_type" character varying(64),
  "status" character varying(64)
);

-- Column comments:
--   id: 主键ID
--   asset_id: 资产ID，关联 wst_asset.id
--   trace_node_id: 挂接后的拓扑节点ID，关联 wst_trace_node.id，pgRouting 查询必须从该节点出发
--   trace_edge_id: 原始挂接边ID，关联 wst_trace_edge.id，仅作为来源记录或展示辅助字段，不作为 pgRouting 起点
--   snap_point_geom: 资产在拓扑网络上的实际挂接点坐标，坐标系SRID=4326
--   asset_point_geom: 资产原始点坐标，主要用于记录资产原始位置
--   distance_m: 资产原始位置到挂接点的距离，单位米
--   snap_type: 挂接类型：node=挂接到已有节点，split_edge=挂接到边中间并拆边，manual=人工指定
--   snap_role: 挂接角色，例如 discharge_point=排放进入点，monitor_point=监测点，intake_point=取水点，gate_control_point=闸口控制点，pipe_inlet=管网入口，pipe_outlet=管网出口，emergency_point=应急点
--   snap_method: 挂接方法：nearest_node=最近节点，nearest_edge=最近边，manual=人工，import=导入
--   snap_status: 挂接状态：candidate=候选，confirmed=已确认，invalid=无效
--   is_primary: 是否主挂接点，同一个资产存在多个挂接点时用于标记主挂接点
--   confidence: 挂接置信度，0-1之间
--   confirmed_by: 确认人
--   confirmed_at: 确认时间
--   metadata_json: 扩展属性JSON，用于存储挂接算法参数、候选边、候选节点等信息
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除
--   snap_node_id: 吸附节点ID
--   snap_edge_id: 吸附边ID
--   snap_distance_m: 吸附距离（米）
--   network_type: 网络类型，例如 river=外部河网，park_pipe=园区管网，park_river=园区内部排污河流，mixed=混合衔接网络
--   status: 状态

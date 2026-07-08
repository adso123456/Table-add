-- Table: public."wst_trace_topology_issue"
-- Table comment: 溯源拓扑问题记录表
CREATE TABLE public."wst_trace_topology_issue" (
  "id" bigint NOT NULL DEFAULT nextval('wst_trace_topology_issue_id_seq'::regclass),
  "issue_type" character varying(64) NOT NULL,
  "issue_name" character varying(128),
  "issue_level" character varying(32) NOT NULL,
  "object_type" character varying(64) NOT NULL,
  "object_id" bigint NOT NULL,
  "object_name" character varying(255),
  "object_code" character varying(128),
  "status" character varying(32) NOT NULL DEFAULT 'pending'::character varying,
  "geom" geometry(Geometry,4326),
  "issue_desc" text,
  "metadata_json" jsonb DEFAULT '{}'::jsonb,
  "remark" text,
  "created_by" character varying(64),
  "created_at" timestamp without time zone DEFAULT now(),
  "updated_by" character varying(64),
  "updated_at" timestamp without time zone DEFAULT now(),
  "del_flag" smallint DEFAULT 0
);

-- Column comments:
--   id: 主键ID
--   issue_type: 问题类型
--   issue_name: 问题名称
--   issue_level: 问题级别
--   object_type: 关联对象类型
--   object_id: 关联对象ID
--   object_name: 关联对象名称
--   object_code: 监控对象编码
--   status: 状态
--   geom: 空间几何数据
--   issue_desc: 问题详细描述
--   metadata_json: 元数据JSON
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 删除标志：0-正常，1-已删除

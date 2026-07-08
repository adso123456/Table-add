-- Table: public."wm_section_info"
-- Table comment: 断面基本信息表
CREATE TABLE public."wm_section_info" (
  "id" bigint,
  "water_body_id" bigint,
  "control_unit_id" bigint,
  "region_id" bigint,
  "section_code" character varying(32),
  "section_name" character varying(255),
  "trans_regional" character varying(32),
  "geom" geometry(Point,4326),
  "section_nature" character varying(4),
  "section_level" character varying(4),
  "manage_type" character varying(64),
  "manage_level" character varying(32),
  "is_examine" character(1),
  "examine_level" character varying(32),
  "examine_city" character varying(32),
  "tributary_trunk" character(1),
  "upstream_section_id" bigint,
  "grid_code" character varying(32),
  "grid_i" character varying(32),
  "grid_j" character varying(32),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 断面id
--   water_body_id: 水体id
--   control_unit_id: 控制单元id
--   region_id: 所属区域id
--   section_code: 断面编码
--   section_name: 断面名称
--   trans_regional: 跨界类型
--   geom: 几何信息
--   section_nature: 断面属性
--   section_level: 断面级别：0-国控、1-省控、2-市控
--   manage_type: 管理类型
--   manage_level: 管理级别
--   is_examine: 考核断面：0 否、1 是
--   examine_level: 考核级别
--   examine_city: 考核城市
--   tributary_trunk: 支流/干流：0 干流、1 支流
--   upstream_section_id: 上游断面id
--   grid_code: 网格号
--   grid_i: 网格I值
--   grid_j: 网格J值
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

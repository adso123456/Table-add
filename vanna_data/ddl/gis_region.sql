-- Table: public."gis_region"
-- Table comment: 区县数据表
CREATE TABLE public."gis_region" (
  "id" bigint NOT NULL,
  "region_code" character varying(32),
  "region_name" character varying(100),
  "control_unit_id" bigint,
  "region_level" character varying(4),
  "parent_code" character varying(60),
  "code" character varying(32),
  "address" character varying(255),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: 主键id
--   region_code: 行政区划编码
--   region_name: 行政区划名称
--   control_unit_id: 管控单元ID
--   region_level: 区划级别
--   parent_code: 父级区划编码
--   code: 编码
--   address: 地址
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

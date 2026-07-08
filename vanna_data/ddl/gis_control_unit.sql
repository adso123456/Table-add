-- Table: public."gis_control_unit"
-- Table comment: 水环境管控单元表
CREATE TABLE public."gis_control_unit" (
  "id" bigint,
  "geom" geometry(MultiPolygon,4326),
  "control_unit_name" character varying(254),
  "area" double precision,
  "control_unit_code" character varying(100),
  "basin" character varying(200),
  "remark" character varying(255),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "create_by" bigint,
  "update_by" bigint
);

-- Column comments:
--   id: 主键
--   geom: 几何信息
--   control_unit_name: 控制单元名称
--   area: 面积（km2）
--   control_unit_code: 控制单元编码
--   basin: 所属流域
--   remark: 备注
--   create_time: 创建时间
--   update_time: 更新时间
--   del_flag: 删除标志：0-正常、1-删除
--   create_by: 创建人
--   update_by: 修改人

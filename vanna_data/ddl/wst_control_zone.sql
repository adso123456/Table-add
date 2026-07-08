-- Table: public."wst_control_zone"
-- Table comment: 水安全溯源模块-三级分区表，用于管理国控断面控制单元、自动站分区、工业园区/分水岭分区
CREATE TABLE public."wst_control_zone" (
  "id" bigint,
  "zone_code" character varying(100),
  "zone_name" character varying(200),
  "zone_level" integer,
  "parent_id" bigint,
  "divide_basis" character varying(100),
  "zone_type" character varying(100),
  "basin_code" character varying(100),
  "river_system_code" character varying(100),
  "sort_no" integer,
  "status" character varying(50),
  "geom" geometry(MultiPolygon,4326),
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone,
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone,
  "del_flag" smallint
);

-- Column comments:
--   id: 主键ID
--   zone_code: 分区编码
--   zone_name: 分区名称
--   zone_level: 分区级别：1=一级国控断面控制单元，2=二级自动站分区，3=三级工业园区/分水岭分区
--   parent_id: 上级分区ID，一级分区为空
--   divide_basis: 分区划分依据，例如国控断面、自动站、工业园区、分水岭、排水片区
--   zone_type: 分区类型，例如 control_unit=控制单元，station_unit=自动站单元，park_unit=园区单元，watershed_unit=分水岭单元
--   basin_code: 流域编码
--   river_system_code: 水系编码
--   sort_no: 排序号
--   status: 状态：active=启用，disabled=停用
--   geom: 分区边界面几何，坐标系SRID=4326
--   metadata_json: 扩展属性JSON，用于存储外部系统ID、原始导入字段等不常用于查询的内容
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除

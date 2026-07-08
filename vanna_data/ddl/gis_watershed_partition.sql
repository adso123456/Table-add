-- Table: public."gis_watershed_partition"
-- Table comment: 空间-流域分区数据
CREATE TABLE public."gis_watershed_partition" (
  "id" bigint,
  "name" character varying(100),
  "name_alias" character varying(100),
  "area" double precision,
  "remark" character varying(255),
  "code" character varying(100),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "geom" geometry(MultiPolygon,4326),
  "version" smallint
);

-- Column comments:
--   id: 主键ID
--   name: 名称
--   name_alias: 别名
--   area: 面积：平方千米
--   remark: 备注
--   code: 编码
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除、1-已删除
--   geom: 图形
--   version: 当前版本：从0开始递增

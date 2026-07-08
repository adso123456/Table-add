-- Table: public."rs_sewage_park_info"
-- Table comment: 污水处理厂-园区配套信息表
CREATE TABLE public."rs_sewage_park_info" (
  "id" bigint,
  "region_code" character varying(32),
  "region_name" character varying(32),
  "sewage_name" character varying(200),
  "sewage_id" bigint,
  "throughput" double precision,
  "park_id" bigint,
  "park_name" character varying(200),
  "lon" double precision,
  "lat" double precision,
  "geom" geometry(Point,4326),
  "remark" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "sewage_type" smallint
);

-- Column comments:
--   id: 主键id
--   region_code: 行政区编码
--   region_name: 行政区名称
--   sewage_name: 污水处理厂名称
--   sewage_id: 污水厂ID
--   throughput: 处理能力（万吨/日）
--   park_id: 配套园区ID
--   park_name: 配套园区名称
--   lon: 经度
--   lat: 纬度
--   geom: 图形信息
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   sewage_type: 污水处理厂类型：0-工业、1-生活

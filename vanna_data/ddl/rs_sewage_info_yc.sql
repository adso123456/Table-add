-- Table: public."rs_sewage_info_yc"
-- Table comment: 污水处理厂信息表：宜昌水环境
CREATE TABLE public."rs_sewage_info_yc" (
  "id" bigint,
  "name" character varying(255),
  "monitor_name" character varying(255),
  "region_code" character varying(32),
  "region_name" character varying(32),
  "emission_type" character(1),
  "supervision_level" character(1),
  "outlet_location" character varying(32),
  "lon" double precision,
  "lat" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "town_flag" boolean,
  "industrial_flag" boolean
);

-- Column comments:
--   id: 主键id
--   name: 企业名称
--   monitor_name: 检测点名称
--   region_code: 行政区编码
--   region_name: 行政区名称
--   emission_type: 排放类型：0-废水
--   supervision_level: 监管级别：0-一般、1-重点
--   outlet_location: 排污口位置
--   lon: 经度
--   lat: 纬度
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记
--   town_flag: 是否城镇污水处理厂
--   industrial_flag: 是否工业污水处理厂

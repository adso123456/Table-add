-- Table: public."wm_station_info_v2"
-- Table comment: 自动站管理
CREATE TABLE public."wm_station_info_v2" (
  "id" bigint,
  "station_code" character varying(255),
  "station_name" character varying(255),
  "short_name" character varying(255),
  "station_type" character varying(10),
  "station_level" character varying(10),
  "iot_connect_type" character varying(8),
  "region_code" character varying(16),
  "region_name" character varying(100),
  "build_state" character varying(30),
  "build_time" timestamp without time zone,
  "water_body_id" bigint,
  "section_id" bigint,
  "equipment_manufacturer" character varying(200),
  "equipment_model" character varying(100),
  "monitor_indicators" character varying(500),
  "monitor_frequency" character varying(100),
  "eight_direction_photo" character varying(500),
  "om_unit" character varying(100),
  "om_person" character varying(100),
  "contact_info" character varying(100),
  "geom" geometry(Point,4326),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "remark" character varying(255),
  "section_name" character varying(100),
  "water_body_name" character varying(150),
  "water_body_type" character varying(10)
);

-- Column comments:
--   id: 主键
--   station_code: 站点编码
--   station_name: 站点名称
--   short_name: 站点简称
--   station_type: 站类型：1-岸基站、2-浮船站
--   station_level: 站点的级别：1-省站、2-市站
--   iot_connect_type: 通信协议类型：0 tcp、1 http、2 mqtt
--   region_code: 行政区编码
--   region_name: 行政区名称
--   build_state: 建站状态：0-待建、1-已建
--   build_time: 建设时间
--   water_body_id: 水体id
--   section_id: 断面id
--   equipment_manufacturer: 设备厂家
--   equipment_model: 设备型号
--   monitor_indicators: 监测指标
--   monitor_frequency: 监测频次
--   eight_direction_photo: 八方图
--   om_unit: 运维单位
--   om_person: 运维人员
--   contact_info: 联系方式
--   geom: 图形信息
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 0未删除,1已删除
--   remark: 备注
--   section_name: 断面名称
--   water_body_name: 水体名称
--   water_body_type: 水体类型：0-河流、1-湖泊

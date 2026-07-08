-- Table: public."wm_meteorological_info"
-- Table comment: 气象自动监测站基本信息表
CREATE TABLE public."wm_meteorological_info" (
  "id" bigint NOT NULL DEFAULT nextval('wm_meteorological_info_id_seq'::regclass),
  "station_code" character varying(255),
  "station_name" character varying(255),
  "short_name" character varying(255),
  "region_code" character varying(16),
  "iot_connect_type" character varying(8),
  "belong_to_city" character varying(60),
  "station_type" character varying(10),
  "build_state" character varying(30),
  "water_type" character varying(20),
  "water_body_id" bigint,
  "section_id" bigint,
  "river_in" bigint DEFAULT 0,
  "pollutant_id" bigint,
  "in_outlet" character(1),
  "river_out" bigint DEFAULT 0,
  "efdc_in" character varying(255) DEFAULT 0,
  "efdc_out" character varying(255) DEFAULT 0,
  "efdc_i" bigint,
  "efdc_j" bigint,
  "head_water" bigint,
  "lake_in" character(1),
  "meteorological_table_name" character varying(255),
  "meteorological_indicator_codes" character varying(255),
  "geom" geometry(Point,4326),
  "frequency" character varying(255),
  "equipments" character varying(255),
  "build_time" date,
  "responsible_person" character varying(255),
  "contact_number" character varying(20),
  "last_maintenance_time" date,
  "img_url" character varying(255),
  "img_name" character varying(100),
  "img_format" character varying(16),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: 监测站点的唯一id
--   station_code: 气象编码
--   station_name: 监测站点名称
--   short_name: 简称
--   region_code: 行政区划代码
--   iot_connect_type: 通信协议类型：0 tcp、1 http、2 mqtt
--   belong_to_city: 归属地市
--   station_type: 站类型(岸基站1|浮船站2)
--   build_state: 建站状态(待建0,已建1)
--   water_type: 水体类型：0 河流、1 湖泊
--   water_body_id: 所属水体id
--   section_id: 断面id
--   river_in: 一维模型来流入汇口
--   pollutant_id: 污染源id
--   in_outlet: 污染源类型为污水处理厂时：0 进水口、1 出水口
--   river_out: 一维模型出水口
--   efdc_in: efdc模型来流入汇口
--   efdc_out: efdc模型出水口
--   efdc_i: 站点所在二维网格I值
--   efdc_j: 站点所在二维网格J值
--   head_water: headwater序号
--   lake_in: 是否为入湖港道：0 否、1 是
--   meteorological_table_name: 气象监测记录表名
--   meteorological_indicator_codes: 气象监测指标编号集合，逗号连接
--   geom: 空间几何数据
--   frequency: 测量频率
--   equipments: 自动站的设备清单
--   build_time: 建设时间
--   responsible_person: 站点责任人
--   contact_number: 责任人联系电话
--   last_maintenance_time: 最近维护时间
--   img_url: 照片地址
--   img_name: 照片名称
--   img_format: 照片格式：img、png等
--   remark: 备注信息
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

-- Table: public."wm_uav_info"
-- Table comment: 大疆无人机基础信息
CREATE TABLE public."wm_uav_info" (
  "id" bigint,
  "code" character varying(100),
  "name" character varying(100),
  "gateway_sn" character varying(100),
  "gateway_callsign" character varying(100),
  "gateway_device_model" character varying(1024),
  "gateway_device_online_status" smallint,
  "gateway_mode_code" integer,
  "gateway_camera_list" character varying(1024),
  "drone_sn" character varying(100),
  "drone_callsign" character varying(100),
  "drone_device_model" character varying(1024),
  "drone_device_online_status" character varying(100),
  "drone_mode_code" integer,
  "drone_camera_list" character varying(1024),
  "gateway_lon" double precision,
  "gateway_lat" double precision,
  "activation_time" bigint,
  "acc_time" integer,
  "humidity" real,
  "job_number" integer,
  "storage_total" integer,
  "storage_used" integer,
  "brand" character varying(100),
  "weight" character varying(100),
  "power" character varying(100),
  "temperature" character varying(100),
  "protect_level" character varying(100),
  "max_height" character varying(100),
  "max_radius" character varying(100),
  "charging_time" character varying(100),
  "cycle_num" character varying(100),
  "duration_time" character varying(100),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   code: 编码
--   name: 名称
--   gateway_sn: 网关SN编码
--   gateway_callsign: 网关名称
--   gateway_device_model: 型号，json格式
--   gateway_device_online_status: 网关在线状态
--   gateway_mode_code: 网关型号编码
--   gateway_camera_list: 网关摄像头列表
--   drone_sn: 无人机SN编码
--   drone_callsign: 无人机名称
--   drone_device_model: 无人机型号
--   drone_device_online_status: 无人机在线状态
--   drone_mode_code: 型号编码
--   drone_camera_list: 无人机摄像头列表
--   gateway_lon: 网关经度
--   gateway_lat: 网关纬度
--   activation_time: 机场激活时间(unix 时间戳)
--   acc_time: 机场累计运行时长
--   humidity: 舱内湿度
--   job_number: 机场累计作业次数
--   storage_total: 存储容量 单位：KB
--   storage_used: 已使用容量 单位：KB
--   brand: 品牌：大疆/纵横昆仑
--   weight: 整机重量
--   power: 功率
--   temperature: 工作温度
--   protect_level: 保护等级
--   max_height: 最大高度
--   max_radius: 最大工作半径
--   charging_time: 充电时间
--   cycle_num: 电池循环次数
--   duration_time: 备用电池续航时间
--   remark: 备注信息
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

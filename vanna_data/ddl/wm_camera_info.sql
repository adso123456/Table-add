-- Table: public."wm_camera_info"
-- Table comment: 摄像头基本信息表
CREATE TABLE public."wm_camera_info" (
  "id" bigint,
  "camera_name" character varying(100),
  "device_type" character varying(100),
  "device_code" character varying(100),
  "device_supplier" character varying(255),
  "device_origin" character varying(100),
  "address" character varying(255),
  "lon" numeric(10,6),
  "lat" numeric(10,6),
  "monitor_subject" character varying(255),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1)
);

-- Column comments:
--   id: 主键
--   camera_name: 摄像头名称
--   device_type: 设备类型
--   device_code: 设备编号
--   device_supplier: 设备厂商
--   device_origin: 设备来源
--   address: 摄像头地址
--   lon: 经度
--   lat: 纬度
--   monitor_subject: 监控对象
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

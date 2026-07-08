-- Table: public."wm_camera_platform"
-- Table comment: 视频平台设备信息表
CREATE TABLE public."wm_camera_platform" (
  "id" bigint,
  "device_code" character varying(20),
  "name" character varying(100),
  "manufacturer" character varying(100),
  "model" character varying(100),
  "transport" character varying(50),
  "stream_mode" character varying(50),
  "ip_address" character varying(100),
  "port" integer,
  "online" smallint,
  "heart_beat_interval" integer,
  "heart_beat_count" integer,
  "charset" character varying(50),
  "lon" double precision,
  "lat" double precision,
  "remark" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1)
);

-- Column comments:
--   id: 主键ID
--   device_code: 设备编码(国标20位)
--   name: 设备名称
--   manufacturer: 厂商
--   model: 型号
--   transport: 传输方式: TCP/UDP
--   stream_mode: 流模式: TCP被动模式/UDP
--   ip_address: 设备IP地址
--   port: 设备端口
--   online: 是否在线: 0-离线, 1-在线
--   heart_beat_interval: 心跳检测间隔(秒)
--   heart_beat_count: 健康检查次数
--   charset: 字符集
--   lon: 经度
--   lat: 纬度
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除, 1-已删除

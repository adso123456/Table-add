-- Table: public."wm_camera_platform"
-- Table comment: 视频平台设备信息表
CREATE TABLE public."wm_camera_platform" (
  "id" bigint NOT NULL,
  "device_code" character varying(20) NOT NULL,
  "name" character varying(100),
  "manufacturer" character varying(100),
  "model" character varying(100),
  "transport" character varying(50) DEFAULT 'TCP'::character varying,
  "stream_mode" character varying(50) DEFAULT 'TCP-PASSIVE'::character varying,
  "ip_address" character varying(100),
  "port" integer,
  "online" smallint DEFAULT 0,
  "heart_beat_interval" integer DEFAULT 60,
  "heart_beat_count" integer DEFAULT 3,
  "charset" character varying(50) DEFAULT 'GB2312'::character varying,
  "lon" double precision,
  "lat" double precision,
  "remark" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character varying(1) DEFAULT '0'::character varying
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

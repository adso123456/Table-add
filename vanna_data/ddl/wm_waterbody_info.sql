-- Table: public."wm_waterbody_info"
-- Table comment: 水体信息实体类
CREATE TABLE public."wm_waterbody_info" (
  "id" bigint NOT NULL,
  "water_body_code" character varying(32),
  "water_body_name" character varying(255),
  "water_body_type" character(1),
  "water_body_function" character varying(255),
  "geom" text,
  "img_url" character varying(255),
  "img_format" character varying(16),
  "img_name" character varying(100),
  "control_unit_id" bigint,
  "basin" character varying(255),
  "length" double precision,
  "width" character varying(255),
  "area" double precision,
  "bend_coefficient" double precision,
  "storage" double precision,
  "country" character varying(255),
  "start_village" character varying(255),
  "end_village" character varying(255),
  "up_stream" character varying(255),
  "down_stream" character varying(255),
  "remark" character varying(255),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: id
--   water_body_code: 水体编码
--   water_body_name: 水体名称
--   water_body_type: 水体类型：0 河流、1 湖泊
--   water_body_function: 水体功能类别
--   geom: 几何信息
--   img_url: 照片地址
--   img_format: 照片格式：img、png等
--   img_name: 照片名称
--   control_unit_id: 所属控制单元id
--   basin: 所在流域
--   length: 水体长度（km）
--   width: 水体宽度（m）
--   area: 水体面积（km2）
--   bend_coefficient: 弯曲系数
--   storage: 蓄水量（m3）
--   start_village: 起点村/社区
--   end_village: 终点村/社区
--   up_stream: 上游水体
--   down_stream: 下游水体
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

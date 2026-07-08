-- Table: public."dc_survey_info"
-- Table comment: 巡回调查-调查后的核查信息
CREATE TABLE public."dc_survey_info" (
  "id" bigint,
  "watershed_partition_id" bigint,
  "title" character varying(50),
  "upload_time" character varying(50),
  "name" character varying(50),
  "type" character varying(50),
  "lon" double precision,
  "lat" double precision,
  "description" character varying(200),
  "image_path" character varying(200),
  "monitor_info" character varying(100),
  "monitor_level" character varying(10),
  "remark" character varying(200),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "survey_type" smallint,
  "image_path_2" character varying(200),
  "image_path_3" character varying(200),
  "task_id" bigint,
  "task_instance_id" bigint
);

-- Column comments:
--   id: 主键ID
--   watershed_partition_id: 流域分区ID
--   title: 标题：对应调研的名称
--   upload_time: 上传时间：每次上传都记录时间  20251128
--   name: 名称
--   type: 类型（工业、规上畜禽、规下畜禽、水产养殖、排污口、污水处理厂、厕污垃、河道情况、其他）
--   lon: 经度
--   lat: 纬度
--   description: 现场核查情况信息（是否有污水产生、污水流向）
--   image_path: 图片地址：图片在minIO存储
--   monitor_info: 监测信息（是否监测，结果如何）
--   monitor_level: 管控级别：一级（常年有水，肯定对水体有影响），二级（下雨时肯定对水体影响），三级（可能有影响），四级（无影响）
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除
--   survey_type: 调查类型：0-excel调查信息、1-word小结
--   image_path_2: 图片2
--   image_path_3: 图片3
--   task_id: APP巡查：任务id
--   task_instance_id: APP巡查：巡查任务实例id

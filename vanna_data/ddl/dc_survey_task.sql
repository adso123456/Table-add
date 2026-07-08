-- Table: public."dc_survey_task"
-- Table comment: 巡查任务表
CREATE TABLE public."dc_survey_task" (
  "id" bigint NOT NULL DEFAULT nextval('dc_survey_task_id_seq'::regclass),
  "title" character varying(255) NOT NULL,
  "survey_time" character varying(20) NOT NULL,
  "watershed_partition_id" bigint NOT NULL,
  "status" integer DEFAULT 0,
  "point_count" integer DEFAULT 0,
  "remark" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character varying(1) DEFAULT '0'::character varying,
  "image_count" integer DEFAULT 0,
  "duration" bigint DEFAULT 0,
  "distance" numeric(20,3) DEFAULT 0.000,
  "current_point_count" integer DEFAULT 0,
  "update_name" character varying(100),
  "cache_id" character varying(100)
);

-- Column comments:
--   id: 主键
--   title: 巡查标题
--   survey_time: 巡查时间: yyyyMMdd
--   watershed_partition_id: 流域分区ID
--   status: 任务状态: 0-进行中, 1-已暂停, 2-已结束
--   point_count: 点位数量
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除
--   image_count: 照片数量
--   duration: 巡查时长: 单位秒
--   distance: 巡查距离: 单位km
--   current_point_count: 本次巡查点位数量: 重新开启后自动清零
--   update_name: 更新人名称：当前巡查人员
--   cache_id: 本地缓存ID：APP端维护

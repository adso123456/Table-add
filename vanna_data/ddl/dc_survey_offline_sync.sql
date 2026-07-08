-- Table: public."dc_survey_offline_sync"
-- Table comment: 离线同步任务表
CREATE TABLE public."dc_survey_offline_sync" (
  "id" bigint,
  "cache_id" character varying(64),
  "sync_status" integer,
  "sync_progress" integer,
  "total_steps" integer,
  "current_step" integer,
  "sync_start_time" timestamp without time zone,
  "sync_end_time" timestamp without time zone,
  "task_id" bigint,
  "sync_result" character varying(500),
  "error_message" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "del_flag" character varying(1)
);

-- Column comments:
--   id: 主键
--   cache_id: 缓存ID：APP端维护，用于关联提交数据
--   sync_status: 同步状态：0-待同步，1-同步中，2-同步成功，3-同步失败
--   sync_progress: 同步进度：0-100
--   total_steps: 总步骤数
--   current_step: 当前步骤
--   sync_start_time: 同步开始时间
--   sync_end_time: 同步结束时间
--   task_id: 任务ID：关联的巡查任务ID
--   sync_result: 同步结果信息
--   error_message: 错误信息
--   create_by: 创建人
--   create_time: 创建时间
--   del_flag: 删除标记：0 未删除、1 已删除

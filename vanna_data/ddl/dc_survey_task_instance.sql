-- Table: public."dc_survey_task_instance"
-- Table comment: 任务实例：记录轨迹、点位的添加
CREATE TABLE public."dc_survey_task_instance" (
  "id" bigint,
  "task_id" bigint,
  "start_time" timestamp without time zone,
  "end_time" timestamp without time zone,
  "duration" bigint,
  "create_time" timestamp without time zone
);

-- Column comments:
--   id: 主键
--   task_id: 任务ID
--   start_time: 执行开始时间
--   end_time: 执行结束时间
--   duration: 执行时长（秒）
--   create_time: 创建时间

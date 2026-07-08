-- Table: public."dc_survey_track"
-- Table comment: 巡查轨迹记录表
CREATE TABLE public."dc_survey_track" (
  "id" bigint NOT NULL DEFAULT nextval('dc_survey_track_id_seq'::regclass),
  "task_id" bigint NOT NULL,
  "lat" double precision NOT NULL,
  "lon" double precision NOT NULL,
  "distance" numeric(20,3) DEFAULT 0.000,
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "num" integer NOT NULL,
  "task_instance_id" bigint
);

-- Column comments:
--   id: 主键
--   task_id: 巡查任务ID
--   lat: 纬度
--   lon: 经度
--   distance: 距离上一个点的距离（米）
--   create_by: 创建人
--   create_time: 创建时间
--   num: 点位编号
--   task_instance_id: 实例ID

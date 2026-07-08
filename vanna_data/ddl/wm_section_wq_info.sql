-- Table: public."wm_section_wq_info"
-- Table comment: 断面水质目标信息表
CREATE TABLE public."wm_section_wq_info" (
  "id" bigint NOT NULL,
  "section_id" bigint,
  "year" bigint,
  "month" bigint,
  "water_quality_target_level" character varying(4),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: id
--   section_id: 断面id
--   year: 年份
--   month: 月份：0,1,2,3,4,5,6,7,8,9,10,11,12（0表示全年）
--   water_quality_target_level: 目标水质
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

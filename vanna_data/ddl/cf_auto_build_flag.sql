-- Table: public."cf_auto_build_flag"
-- Table comment: 主键id
CREATE TABLE public."cf_auto_build_flag" (
  "id" bigint NOT NULL,
  "manual_auto" character(1) NOT NULL,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0
);

-- Column comments:
--   id: 主键id
--   manual_auto: 0 手动处理、1 自动处理
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

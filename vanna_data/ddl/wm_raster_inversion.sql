-- Table: public."wm_raster_inversion"
-- Table comment: 遥感反演结果表（合并版）
CREATE TABLE public."wm_raster_inversion" (
  "id" bigint,
  "record_id" bigint,
  "indicator_code" bigint,
  "indicator_name" character varying(60),
  "inversion_type" character varying(20),
  "file_path" character varying(500),
  "l1_area" double precision,
  "l2_area" double precision,
  "l3_area" double precision,
  "l4_area" double precision,
  "l5_area" double precision,
  "l6_area" double precision,
  "unit" character varying(50),
  "service_url" text,
  "data_time" timestamp without time zone,
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   record_id: 遥感反演结果记录ID
--   indicator_code: 遥感监测分析项编码
--   indicator_name: 指标项名称
--   inversion_type: 反演类型：water_environment-水环境，algalbloom-水生态，landuse-土地利用
--   file_path: 反演文件路径
--   l1_area: I类/浮叶挺水植被/背景面积
--   l2_area: II类/沉水植被/耕地面积
--   l3_area: III类/水华/园地面积
--   l4_area: IV类/水体/林地面积
--   l5_area: V类/水体面积
--   l6_area: 劣V类/建设用地面积
--   unit: 面积单位
--   service_url: 服务地址
--   data_time: 数据日期
--   create_time: 创建时间
--   update_time: 更新时间
--   del_flag: 删除标志

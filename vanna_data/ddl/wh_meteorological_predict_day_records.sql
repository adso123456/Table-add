-- Table: public."wh_meteorological_predict_day_records"
-- Table comment: 气象预报日记录表
CREATE TABLE public."wh_meteorological_predict_day_records" (
  "id" text,
  "station_id" bigint,
  "winddirect_10m_24h" double precision,
  "winddirect8_10m_24h" character varying(16),
  "winddirect16_10m_24h" character varying(16),
  "hum_2m_24h" double precision,
  "hum_2m_24h_min" double precision,
  "hum_2m_24h_max" double precision,
  "stapress_24h" double precision,
  "pressure_24h" double precision,
  "p850inver_24h" double precision,
  "p925inver_24h" double precision,
  "swdown_24h" double precision,
  "glw_24h" double precision,
  "height_24h" double precision,
  "rain_24h_total" double precision,
  "dewpoint_24h" double precision,
  "lowcloud_24h" double precision,
  "midcloud_24h" double precision,
  "highcloud_24h" double precision,
  "totalcloud_24h" double precision,
  "tem_2m_24h" double precision,
  "tem_2m_24h_min" double precision,
  "tem_2m_24h_max" double precision,
  "visib_24h" double precision,
  "pbl_24h" double precision,
  "pbl_24h_min" double precision,
  "pbl_24h_max" double precision,
  "windspeed_10m_24h" double precision,
  "windspeed_10m_24h_min" double precision,
  "windspeed_10m_24h_max" double precision,
  "predictiontime" timestamp without time zone,
  "time" bigint,
  "predictioninterval" bigint,
  "datadate" timestamp without time zone,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: id
--   station_id: 所属站点id
--   winddirect_10m_24h: 10米风向（24小时平均）
--   winddirect8_10m_24h: 10米8方位风向（24小时）
--   winddirect16_10m_24h: 10米16方位风向（24小时）
--   hum_2m_24h: 2米湿度（24小时平均）
--   hum_2m_24h_min: 2米湿度最小值（24小时）
--   hum_2m_24h_max: 2米湿度最大值（24小时）
--   stapress_24h: 地面气压（24小时平均）
--   pressure_24h: 海平面气压（24小时平均）
--   p850inver_24h: 850hPa逆温层高度（24小时）
--   p925inver_24h: 925hPa逆温层高度（24小时）
--   swdown_24h: 短波辐射通量（24小时平均）
--   glw_24h: 长波辐射通量（24小时平均）
--   height_24h: 边界层高度（24小时）
--   rain_24h_total: 24小时总降雨量
--   dewpoint_24h: 露点温度（24小时）
--   lowcloud_24h: 低云量（24小时）
--   midcloud_24h: 中云量（24小时）
--   highcloud_24h: 高云量（24小时）
--   totalcloud_24h: 总云量（24小时）
--   tem_2m_24h: 2米温度（24小时平均）
--   tem_2m_24h_min: 2米温度最小值（24小时）
--   tem_2m_24h_max: 2米温度最大值（24小时）
--   visib_24h: 能见度（24小时）
--   pbl_24h: 行星边界层高度（24小时平均）
--   pbl_24h_min: 行星边界层高度最小值（24小时）
--   pbl_24h_max: 行星边界层高度最大值（24小时）
--   windspeed_10m_24h: 10米风速（24小时平均）
--   windspeed_10m_24h_min: 10米风速最小值（24小时）
--   windspeed_10m_24h_max: 10米风速最大值（24小时）
--   predictiontime: 预测时间
--   time: 预报时次,如08时、20时
--   predictioninterval: 预测间隔（小时）
--   datadate: 数据日期
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

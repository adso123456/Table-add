-- Table: public."wh_meteorological_predict_hour_records"
-- Table comment: 气象预报小时记录表
CREATE TABLE public."wh_meteorological_predict_hour_records" (
  "id" text,
  "station_id" bigint,
  "winddirect_10m_1h" double precision,
  "winddirect8_10m_1h" character varying(16),
  "winddirect16_10m_1h" character varying(16),
  "windspeed_10m_1h" double precision,
  "tem_2m_1h" double precision,
  "hum_2m_1h" double precision,
  "dewpoint_1h" double precision,
  "dtem_2m_1h" double precision,
  "dtem_2m_3h" double precision,
  "dtem_2m_6h" double precision,
  "dtem_2m_12h" double precision,
  "dtem_2m_24h" double precision,
  "rain_1h" double precision,
  "rain_3h" double precision,
  "rain_6h" double precision,
  "rain_12h" double precision,
  "rain_24h" double precision,
  "lowcloud_1h" double precision,
  "midcloud_1h" double precision,
  "highcloud_1h" double precision,
  "totalcloud_1h" double precision,
  "pbl_1h" double precision,
  "height_1h" double precision,
  "pressure_1h" double precision,
  "stapress_1h" double precision,
  "glw_1h" double precision,
  "swdown_1h" double precision,
  "p850inver_1h" double precision,
  "p925inver_1h" double precision,
  "visib_1h" double precision,
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
--   winddirect_10m_1h: 10米风向（小时）
--   winddirect8_10m_1h: 10米8方位风向（小时）
--   winddirect16_10m_1h: 10米16方位风向（小时）
--   windspeed_10m_1h: 10米风速（小时）
--   tem_2m_1h: 2米温度（小时）
--   hum_2m_1h: 2米湿度（小时）
--   dewpoint_1h: 露点温度（小时）
--   dtem_2m_1h: 2米温度1小时变化
--   dtem_2m_3h: 2米温度3小时变化
--   dtem_2m_6h: 2米温度6小时变化
--   dtem_2m_12h: 2米温度12小时变化
--   dtem_2m_24h: 2米温度24小时变化
--   rain_1h: 小时降雨量
--   rain_3h: 3小时累计降雨量
--   rain_6h: 6小时累计降雨量
--   rain_12h: 12小时累计降雨量
--   rain_24h: 24小时累计降雨量
--   lowcloud_1h: 低云量（小时）
--   midcloud_1h: 中云量（小时）
--   highcloud_1h: 高云量（小时）
--   totalcloud_1h: 总云量（小时）
--   pbl_1h: 行星边界层高度（小时）
--   height_1h: 边界层高度（小时）
--   pressure_1h: 海平面气压（小时）
--   stapress_1h: 地面气压（小时）
--   glw_1h: 长波辐射通量（小时）
--   swdown_1h: 短波辐射通量（小时）
--   p850inver_1h: 850hPa逆温层高度（小时）
--   p925inver_1h: 925hPa逆温层高度（小时）
--   visib_1h: 能见度（小时）
--   predictiontime: 预测时间
--   time: 预报时次,如08时、20时
--   predictioninterval: 预测间隔（小时）
--   datadate: 数据日期
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

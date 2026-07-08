-- Table: public."se_watershed"
-- Table comment: 流域产值信息：年统计值
CREATE TABLE public."se_watershed" (
  "id" bigint NOT NULL,
  "region_code" character varying(100),
  "total_population" double precision,
  "total_product_value" double precision,
  "total_river_area" double precision,
  "total_watershed_area" double precision,
  "water_depth_avg" double precision,
  "runoff_value" double precision,
  "statistic_year" bigint,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1) DEFAULT 0,
  "name" character varying(100),
  "mark" character varying(255)
);

-- Column comments:
--   id: 主键ID
--   region_code: 所属区域Code
--   total_population: 总人口
--   total_product_value: 地区生产总值
--   total_river_area: 水面面积：k㎡
--   total_watershed_area: 流域面积：k㎡
--   water_depth_avg: 年平均水深：m
--   runoff_value: 径流量：亿m³
--   statistic_year: 统计年份
--   update_by: 创建人
--   update_time: 创建时间
--   del_flag: 删除标记：0 未删除、1 已删除
--   name: 流域名称
--   mark: 备注

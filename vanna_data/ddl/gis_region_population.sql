-- Table: public."gis_region_population"
-- Table comment: 行政区人口统计表
CREATE TABLE public."gis_region_population" (
  "id" bigint,
  "region_id" bigint,
  "city_population" double precision,
  "city_area" double precision,
  "city_quantity" double precision,
  "rural_population" double precision,
  "rural_area" double precision,
  "rural_quantity" double precision,
  "year" bigint,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   region_id: 区域ID
--   city_population: 城镇人口
--   city_area: 城镇面积
--   city_quantity: 城镇数量
--   rural_population: 农村人口
--   rural_area: 农村面积
--   rural_quantity: 农村数量
--   year: 年份
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除

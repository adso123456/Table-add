-- Table: public."gis_poi"
-- Table comment: 主键id
CREATE TABLE public."gis_poi" (
  "id" bigint,
  "code" bigint,
  "name" character varying(100),
  "address" character varying(255),
  "category" character varying(100),
  "region_code" character varying(32),
  "region_province" character varying(30),
  "region_city" character varying(50),
  "lon" double precision,
  "lat" double precision,
  "telephone" character varying(11),
  "remark" character varying(255),
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "create_by" bigint,
  "update_by" bigint
);

-- Column comments:
--   id: 主键id
--   code: poi标识码
--   name: 名称
--   address: 地址
--   category: 分类
--   region_code: 行政区编码
--   region_province: 行政区省
--   region_city: 行政区城市
--   lon: 经度
--   lat: 纬度
--   telephone: 电话
--   remark: 备注
--   create_time: 创建时间
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   create_by: 创建人
--   update_by: 修改人

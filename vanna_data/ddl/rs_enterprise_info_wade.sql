-- Table: public."rs_enterprise_info_wade"
-- Table comment: 污染源自动监管涉水企业：宜昌水环境
CREATE TABLE public."rs_enterprise_info_wade" (
  "id" bigint,
  "name" character varying(100),
  "address" character varying(255),
  "region_code" character varying(32),
  "region_name" character varying(32),
  "liaison" character varying(32),
  "liaison_tel" character varying(100),
  "supervision_level" smallint,
  "industry_type" character varying(32),
  "lon" double precision,
  "lat" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   name: 污染源名称
--   address: 污染源地址
--   region_code: 行政区编码
--   region_name: 行政区名称
--   liaison: 环保联系人
--   liaison_tel: 环保联系人电话
--   supervision_level: 监管级别：0-一般、1-重点
--   industry_type: 行业类型
--   lon: 经度
--   lat: 纬度
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记

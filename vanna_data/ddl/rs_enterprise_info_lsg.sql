-- Table: public."rs_enterprise_info_lsg"
-- Table comment: 湖北省磷石膏尾矿库企业信息表：宜昌水环境
CREATE TABLE public."rs_enterprise_info_lsg" (
  "id" bigint,
  "name" character varying(100),
  "mine_name" character varying(100),
  "enterprise" character varying(100),
  "city" character varying(32),
  "county" character varying(32),
  "address" character varying(255),
  "region_code" character varying(32),
  "region_name" character varying(32),
  "out_type" character varying(32),
  "design_storage" double precision,
  "existed_storage" double precision,
  "floor_area" double precision,
  "product_status" character varying(32),
  "lon" double precision,
  "lat" double precision,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "product_capacity" double precision
);

-- Column comments:
--   id: 主键id
--   name: 磷石膏库名称
--   mine_name: 矿山名称
--   enterprise: 所属企业
--   city: 市
--   county: 县
--   address: 污染源地址
--   region_code: 行政区编码
--   region_name: 行政区名称
--   out_type: 排渣方式
--   design_storage: 设计库容（单位：万立方米）
--   existed_storage: 现有堆量（单位：万立方米）
--   floor_area: 占地面积（单位平方公里）
--   product_status: 目前生产情况
--   lon: 经度
--   lat: 纬度
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记
--   product_capacity: 磷酸产能（万吨/年）

-- Table: public."rs_livestock_info_yc"
-- Table comment: 规模化畜禽养殖场-宜昌水环境
CREATE TABLE public."rs_livestock_info_yc" (
  "id" bigint,
  "name" character varying(100),
  "name_old" character varying(100),
  "representative" character varying(100),
  "community_code" character varying(100),
  "year" character varying(10),
  "credit_code" character varying(100),
  "organize_code" character varying(100),
  "city" character varying(32),
  "county" character varying(32),
  "town" character varying(32),
  "village" character varying(255),
  "region_code" character varying(32),
  "region_name" character varying(32),
  "liaison" character varying(32),
  "liaison_tel" character varying(32),
  "livestock_type" character varying(20),
  "clean_type" character varying(20),
  "intake_type" character varying(20),
  "water_store_type" character varying(20),
  "water_store_outlet" character varying(20),
  "water_store_area" double precision,
  "water_store_volume" double precision,
  "n_technique_1" character varying(50),
  "n_technique_2" character varying(50),
  "n_facility_1" character varying(50),
  "n_facility_2" character varying(50),
  "n_deal_use_scale" character varying(50),
  "n_scale_1" double precision,
  "n_scale_2" double precision,
  "n_scale_3" double precision,
  "n_scale_4" double precision,
  "n_scale_5" double precision,
  "n_scale_6" double precision,
  "n_scale_7" double precision,
  "n_scale_8" double precision,
  "n_scale_9" double precision,
  "n_scale_10" double precision,
  "f_store_flag1" smallint,
  "f_store_flag2" smallint,
  "f_store_volume" double precision,
  "f_technique_1" character varying(50),
  "f_technique_2" character varying(50),
  "f_deal_use_scale" character varying(50),
  "f_scale_1" double precision,
  "f_scale_2" double precision,
  "f_scale_3" double precision,
  "f_scale_4" double precision,
  "f_scale_5" double precision,
  "f_scale_6" double precision,
  "f_scale_7" double precision,
  "f_scale_8" double precision,
  "f_scale_9" double precision,
  "f_scale_10" double precision,
  "water_name" character varying(32),
  "water_code" character varying(32),
  "glbh_flag" smallint,
  "fzr" character varying(32),
  "tjr" character varying(32),
  "shr" character varying(32),
  "bcrq" timestamp without time zone,
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
--   name: 养殖场名称
--   name_old: 曾用名
--   representative: 法定代表人
--   community_code: 普查小区代码
--   year: 年份
--   credit_code: 统一社会信用代码
--   organize_code: 组织机构代码
--   city: 市
--   county: 县
--   town: 乡镇
--   village: 村、街、门牌号
--   region_code: 行政区编码
--   region_name: 行政区名称
--   liaison: 联系人
--   liaison_tel: 联系人电话
--   livestock_type: 养殖类型
--   clean_type: 圈舍清理方式
--   intake_type: 圈舍通风方式
--   water_store_type: 原水存储设施类型
--   water_store_outlet: 原水存储设施池口方式
--   water_store_area: 原水存储设施池口面积（平方米）
--   water_store_volume: 原水存储设施池口体积（立方米）
--   n_technique_1: 尿液废水处理工艺
--   n_technique_2: 尿液废水处理工艺其他
--   n_facility_1: 尿液废水处理设施
--   n_facility_2: 尿液废水处理设施其他
--   n_deal_use_scale: 尿液废水处理利用方式及比例
--   n_scale_1: 尿液废水处理_肥水利用比例
--   n_scale_2: 尿液废水处理_沼液还田比例
--   n_scale_3: 尿液废水处理_场内生产液体有机肥比例
--   n_scale_4: 尿液废水处理_异位发酵床比例
--   n_scale_5: 尿液废水处理_鱼塘养殖比例
--   n_scale_6: 尿液废水处理_场区循环利用比例
--   n_scale_7: 尿液废水处理_委托处理比例
--   n_scale_8: 尿液废水处理_达标排放比例
--   n_scale_9: 尿液废水处理_直接排放比例
--   n_scale_10: 尿液废水处理_其他
--   f_store_flag1: 粪便存储设施是否防水
--   f_store_flag2: 粪便存储设施是否防渗
--   f_store_volume: 粪便存储设施容积_立方米
--   f_technique_1: 粪便处理工艺
--   f_technique_2: 粪便处理工艺其他
--   f_deal_use_scale: 粪便处理利用方式及比例
--   f_scale_1: 粪便处理利用_农家肥比例
--   f_scale_2: 粪便处理利用_场内生产有机肥比例
--   f_scale_3: 粪便处理利用_沼泽还田比例
--   f_scale_4: 粪便处理利用_生产牛床垫料比例
--   f_scale_5: 粪便处理利用_作为栽培基质比例
--   f_scale_6: 粪便处理利用_作为燃料比例
--   f_scale_7: 粪便处理利用_鱼塘养殖比例
--   f_scale_8: 粪便处理利用_委托处理比例
--   f_scale_9: 粪便处理利用_场外丢弃比例
--   f_scale_10: 粪便处理利用_其他方式
--   water_name: 受纳水体名称
--   water_code: 受纳水体代码
--   glbh_flag: 养殖场是否有锅炉
--   fzr: 单位负责人
--   tjr: 统计负责人
--   shr: 审核人
--   bcrq: 报出日期
--   lon: 经度
--   lat: 纬度
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记

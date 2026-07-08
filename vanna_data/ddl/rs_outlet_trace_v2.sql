-- Table: public."rs_outlet_trace_v2"
-- Table comment: 排污口溯源
CREATE TABLE public."rs_outlet_trace_v2" (
  "id" bigint,
  "outlet_id" bigint,
  "primary_entity_name" character varying(200),
  "other_entity_name" character varying(200),
  "address" character varying(500),
  "primary_contact" character varying(100),
  "primary_phone" character varying(100),
  "discharge_permit_no" character varying(100),
  "credit_code" character varying(100),
  "emission_standard" character varying(200),
  "has_toxic_pollutant" character varying(10),
  "wastewater_type" character varying(100),
  "other_wastewater_type" character varying(200),
  "is_above_scale" character varying(10),
  "approval_status" character varying(200),
  "pollutant_info" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "geom" geometry(Point,4326),
  "outlet_name" character varying(200)
);

-- Column comments:
--   id: 主键ID
--   outlet_id: 关联排污口ID
--   primary_entity_name: 主要责任主体名称
--   other_entity_name: 其他责任主体名称
--   address: 详细地址
--   primary_contact: 主要责任主体联系人
--   primary_phone: 主要责任主体联系电话
--   discharge_permit_no: 排污许可证号或排污登记号
--   credit_code: 统一信用代码
--   emission_standard: 排放标准
--   has_toxic_pollutant: 是否排放有毒有害污染物
--   wastewater_type: 污水类型
--   other_wastewater_type: 其他污水类型
--   is_above_scale: 是否为规模以上排污口
--   approval_status: 审批登记情况
--   pollutant_info: 污染物及排放量(JSON)
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   geom: 排污口所在位置
--   outlet_name: 排污口名称

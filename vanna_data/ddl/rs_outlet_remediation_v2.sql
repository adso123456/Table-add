-- Table: public."rs_outlet_remediation_v2"
-- Table comment: 排污口整治
CREATE TABLE public."rs_outlet_remediation_v2" (
  "id" bigint,
  "outlet_id" bigint,
  "is_remediated" character varying(10),
  "remediation_type" character varying(100),
  "remediation_video" character varying(500),
  "supporting_docs" character varying(500),
  "is_standardized" character varying(10),
  "standardization_content" character varying(500),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character varying(1),
  "outlet_name" character varying(200)
);

-- Column comments:
--   id: 主键ID
--   outlet_id: 关联排污口ID
--   is_remediated: 是否完成整治
--   remediation_type: 整治类型
--   remediation_video: 整治视频
--   supporting_docs: 证明材料
--   is_standardized: 是否完成规范化建设
--   standardization_content: 规范化建设内容
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 修改人
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   outlet_name: 排污口名称

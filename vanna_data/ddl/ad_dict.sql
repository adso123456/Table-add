-- Table: public."ad_dict"
-- Table comment: 数据字典
CREATE TABLE public."ad_dict" (
  "row_id" bigint,
  "list_type" character varying(32),
  "list_type_desc" character varying(255),
  "item_code" character varying(32),
  "item_name" character varying(100),
  "taxis_no" integer,
  "origin_flag" character(1),
  "origin_app" character varying(32),
  "modification_num" integer,
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "create_by" bigint,
  "update_by" bigint
);

-- Column comments:
--   row_id: ROW_ID
--   list_type: 列表类型
--   list_type_desc: 列表描述
--   item_code: 列表项代码
--   item_name: 列表项名称
--   taxis_no: 排序码
--   origin_flag: 数据来源的标志：[]或[I]-(Input)系统录入;[O]-(Out)外部接口导入;[S]-(System)系统保留。本标志不能挪为它用。
--   origin_app: 数据来源应用的代码
--   modification_num: 记录修改次数
--   create_time: 创建时间
--   update_time: 修改时间
--   del_flag: 删除标志：0-正常，1-已删除
--   create_by: 创建人
--   update_by: 修改人

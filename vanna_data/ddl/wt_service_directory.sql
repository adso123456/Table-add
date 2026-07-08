-- Table: public."wt_service_directory"
-- Table comment: 主键id
CREATE TABLE public."wt_service_directory" (
  "id" bigint,
  "node_type" character(1),
  "code" character varying(255),
  "pid" bigint,
  "id_path" character varying(255),
  "name" character varying(255),
  "rest_url" character varying(255),
  "service_type" character(1),
  "x_min" character varying(32),
  "x_max" character varying(32),
  "y_min" character varying(32),
  "y_max" character varying(32),
  "srs" character varying(128),
  "scale" character varying(32),
  "method" character(1),
  "geometry_type" character(1),
  "weidu" character(1),
  "sort" bigint,
  "check_type" character(1),
  "remark" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1)
);

-- Column comments:
--   id: 主键id
--   node_type: 节点类型：0 目录、1 服务
--   code: code 唯一
--   pid: 父id
--   id_path: id路径，逗号连接
--   name: 服务名称
--   rest_url: 接口服务地址
--   service_type: 服务类型：0 WMS、1 WMTS、2 REST接口 、3 公司出图服务 HGTWMS 4 arcgis服务、5 geoserver服务
--   x_min: x最小值
--   x_max: x最大值
--   y_min: y最小值
--   y_max: y最大值
--   srs: 坐标系，WKID表示
--   scale: 在一定比例尺下才显示
--   method: 接口服务请求方式：0 GET、1 POST
--   geometry_type: 几何类型：1 点、2 线、3 面、4 三维模型、5 影像
--   weidu: 维度：0 二维、1 三维
--   sort: 排序号
--   check_type: 是否选中：0 未选中、1 已选中
--   remark: 备注
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记：0 未删除、1 已删除

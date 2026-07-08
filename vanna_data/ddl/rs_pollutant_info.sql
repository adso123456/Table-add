-- Table: public."rs_pollutant_info"
-- Table comment: 企业污染源排口信息表：宜昌污染源在线平台
CREATE TABLE public."rs_pollutant_info" (
  "id" bigint,
  "xh" character varying(255),
  "jcdbh" character varying(50),
  "jcdmc" character varying(200),
  "wrybh" character varying(50),
  "pwkwz" character varying(200),
  "jgjb" character varying(10),
  "sfjsk" character varying(50),
  "sfzs" character(1),
  "zsxs" character varying(50),
  "jd" double precision,
  "wd" double precision,
  "geom" geometry(Point,4326),
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_by" bigint,
  "update_time" timestamp without time zone,
  "del_flag" character(1),
  "record_type" smallint,
  "wrlx" character varying(10),
  "outlet_id" bigint
);

-- Column comments:
--   id: 主键
--   xh: 序号：用于查询数据=driveId
--   jcdbh: 监测点编号
--   jcdmc: 监测点名称
--   wrybh: 污染源编号
--   pwkwz: 排放口位置
--   jgjb: 监管级别：ZD-重点、YB-一般
--   sfjsk: 是否进水口（0：否；1：是）
--   sfzs: 是否烧结等无需折算（0：否；1：是）
--   zsxs: 折算系数
--   jd: 经度
--   wd: 纬度
--   geom: 图形
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除、1-已删除
--   record_type: 记录类型：0-自动、1-手动
--   wrlx: 污染类型：FS-废水、FQ-废气
--   outlet_id: 污染源id

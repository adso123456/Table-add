-- Table: public."layer_reservoir_provincial"
-- Table comment: 省控水库
CREATE TABLE public."layer_reservoir_provincial" (
  "id" integer,
  "geom" geometry(MultiPolygon,4326),
  "objectid" bigint,
  "cc" character varying(8),
  "gb" character varying(16),
  "bas" character varying(16),
  "name" character varying(64),
  "period" character varying(16),
  "type" character varying(32),
  "wq" character varying(8),
  "aheight" double precision,
  "parea" double precision,
  "ec" character varying(16),
  "grade" character varying(8),
  "length" double precision,
  "mheight" double precision,
  "sdtf" character varying(4),
  "shrc" character varying(64),
  "vol" double precision,
  "featid" character varying(16),
  "areacode" bigint,
  "changetype" integer,
  "shape_leng" double precision,
  "shape_area" double precision
);

-- Column comments:
--   id: 主键ID
--   geom: 空间几何数据
--   objectid: 对象唯一标识
--   cc: 行政区划编码
--   gb: 国标编码
--   bas: 流域编码
--   name: 名称
--   period: 时期/阶段
--   type: 类型
--   wq: 水质类别
--   aheight: 坝高
--   parea: 永久占地面积
--   ec: 生态分区编码
--   grade: 等级/级别
--   length: 长度
--   mheight: 最大坝高
--   sdtf: 水系特征码
--   shrc: 所属河湖编码
--   vol: 库容
--   featid: 要素唯一标识
--   areacode: 行政区划代码
--   changetype: 变更类型
--   shape_leng: 要素长度
--   shape_area: 要素面积

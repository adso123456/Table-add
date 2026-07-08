-- Table: public."layer_river_provincial"
-- Table comment: 省级河流空间表
CREATE TABLE public."layer_river_provincial" (
  "geom" geometry(MultiLineString,4326),
  "cc" character varying(8),
  "gb" character varying(16),
  "bas" character varying(16),
  "type" character varying(32),
  "ec" character varying(16),
  "grade" character varying(8),
  "length" double precision,
  "period" character varying(16),
  "shrc" character varying(64),
  "sdtf" character varying(4),
  "width" double precision,
  "featid" character varying(16),
  "areacode" bigint,
  "name" character varying(64),
  "changetype" integer,
  "id" integer
);

-- Column comments:
--   geom: 空间几何数据
--   cc: 行政区划编码
--   gb: 国标编码
--   bas: 流域编码
--   type: 类型
--   ec: 生态分区编码
--   grade: 等级/级别
--   length: 长度
--   period: 时期/阶段
--   shrc: 所属河湖编码
--   sdtf: 水系特征码
--   width: 宽度
--   featid: 要素唯一标识
--   areacode: 行政区划代码
--   name: 名称
--   changetype: 变更类型
--   id: 主键ID

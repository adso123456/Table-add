-- Table: public."rs_pollutant_enterprise"
-- Table comment: 污染源企业信息表：宜昌污染源在线平台企业信息
CREATE TABLE public."rs_pollutant_enterprise" (
  "id" bigint NOT NULL,
  "wrybh" character varying(50) NOT NULL,
  "wrymc" character varying(100),
  "tyshxydm" character varying(50),
  "zzjgdm" character varying(50),
  "pwxkzbh" character varying(50),
  "frmc" character varying(50),
  "lxdh" character varying(50),
  "zcdz" character varying(500),
  "jycsdz" character varying(500),
  "jd" double precision,
  "wd" double precision,
  "hblxr" character varying(50),
  "hbrlxdh" character varying(50),
  "ssqx" character varying(50),
  "hymc" character varying(50),
  "zdlxmc" character varying(200),
  "jgjb" character varying(50),
  "ywgs" character varying(255),
  "geom" geometry(Point,4326),
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "update_by" bigint,
  "update_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  "del_flag" character(1) DEFAULT '0'::bpchar,
  "record_type" smallint DEFAULT 0,
  "ssqxmc" character varying(100)
);

-- Column comments:
--   id: 主键
--   wrybh: 污染源编号
--   wrymc: 污染源名称
--   tyshxydm: 统一社会信用代码
--   zzjgdm: 组织机构代码
--   pwxkzbh: 排污许可证编号
--   frmc: 法人名称
--   lxdh: 联系电话
--   zcdz: 注册地址
--   jycsdz: 经营场所地址
--   jd: 经度
--   wd: 纬度
--   hblxr: 环保联系人
--   hbrlxdh: 环保联系人电话
--   ssqx: 所属区县
--   hymc: 行业名称
--   zdlxmc: 重点污染源类型名称
--   jgjb: 监管级别（代码集：ZXJC_WRYJGJB）：ZDWRY、YBWRY
--   ywgs: 运维公司
--   geom: 图形
--   create_by: 创建人
--   create_time: 创建时间
--   update_by: 更新人
--   update_time: 更新时间
--   del_flag: 删除标记: 0-未删除、1-已删除
--   record_type: 记录类型：0-自动、1-手动
--   ssqxmc: 区县名称

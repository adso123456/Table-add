-- Table: public."wst_asset"
-- Table comment: 水安全溯源模块-统一资产表，存储断面、站点、排口、企业、园区、闸坝、管线、摄像头、事故池等可上图、可查询、可关联对象
CREATE TABLE public."wst_asset" (
  "id" bigint,
  "asset_code" character varying(100),
  "asset_name" character varying(200),
  "asset_type" character varying(100),
  "asset_subtype" character varying(100),
  "zone_id" bigint,
  "source_system" character varying(100),
  "source_id" character varying(200),
  "administrative_region_code" character varying(100),
  "administrative_region_name" character varying(200),
  "address" character varying(500),
  "river_name" character varying(200),
  "river_code" character varying(100),
  "basin_code" character varying(100),
  "longitude" numeric(12,8),
  "latitude" numeric(12,8),
  "elevation" numeric(12,3),
  "status" character varying(50),
  "geom" geometry(Geometry,4326),
  "metadata_json" jsonb,
  "remark" text,
  "created_by" character varying(100),
  "created_at" timestamp without time zone,
  "updated_by" character varying(100),
  "updated_at" timestamp without time zone,
  "del_flag" smallint
);

-- Column comments:
--   id: 主键ID
--   asset_code: 资产编码
--   asset_name: 资产名称
--   asset_type: 资产类型，例如 national_section、provincial_section、auto_station、outfall、water_enterprise、chemical_park、wwtp、water_intake、camera、accident_pool、park_pipe、park_river
--   asset_subtype: 资产子类型，用于进一步细分资产类型，例如雨水排口、污水排口、永久闸、临时闸、主管、支管
--   zone_id: 默认所属分区ID，关联 wst_control_zone.id，用于列表过滤、统计、权限、地图筛选
--   source_system: 数据来源系统，例如 manual=手工录入，permit=排污许可系统，monitor=监测系统，gis=GIS导入
--   source_id: 来源系统中的原始ID
--   administrative_region_code: 行政区划编码
--   administrative_region_name: 行政区划名称
--   address: 详细地址
--   river_name: 关联河流名称
--   river_code: 关联河流编码
--   basin_code: 所属流域编码
--   longitude: 经度
--   latitude: 纬度
--   elevation: 高程，单位米
--   status: 状态：active=启用，disabled=停用，candidate=候选，invalid=无效
--   geom: 资产空间几何，点、线、面均可，坐标系SRID=4326
--   metadata_json: 扩展属性JSON，用于存储行业类型、污染物类型、许可证号、联系人、监测因子等扩展信息
--   remark: 备注
--   created_by: 创建人
--   created_at: 创建时间
--   updated_by: 更新人
--   updated_at: 更新时间
--   del_flag: 逻辑删除标记：0=未删除，1=已删除

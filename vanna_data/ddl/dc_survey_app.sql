-- Table: public."dc_survey_app"
-- Table comment: APP安装包版本管理表
CREATE TABLE public."dc_survey_app" (
  "id" bigint NOT NULL DEFAULT nextval('dc_survey_app_id_seq'::regclass),
  "version_code" character varying(50) NOT NULL,
  "version_name" character varying(100) NOT NULL,
  "update_type" smallint DEFAULT 2,
  "download_url" character varying(500) NOT NULL,
  "file_size" bigint NOT NULL,
  "file_md5" character varying(32) NOT NULL,
  "update_log" text,
  "platform_type" smallint DEFAULT 1,
  "create_by" bigint,
  "create_time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

-- Column comments:
--   id: 主键ID
--   version_code: APP版本号：V1.0.0、1.0.0、100
--   version_name: APP版本名称: 如果有多个APP保证每一类名称一致
--   update_type: 更新类型：1-强制更新，2-可选更新
--   download_url: 安装包下载地址
--   file_size: 安装包文件大小（字节）
--   file_md5: 安装包MD5值，用于校验文件完整性
--   update_log: 更新日志
--   platform_type: 平台类型：1-Android，2-iOS
--   create_by: 创建人
--   create_time: 创建时间

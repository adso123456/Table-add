-- Table: public."dc_survey_offline_upload"
-- Table comment: 文件上传缓存表 - 支持断点续传和本地文件缓存
CREATE TABLE public."dc_survey_offline_upload" (
  "id" bigint,
  "cache_id" character varying(64),
  "file_md5" character varying(32),
  "file_type" character varying(20),
  "file_name" character varying(255),
  "file_size" bigint,
  "uploaded_size" bigint,
  "total_chunks" integer,
  "uploaded_chunks" text,
  "file_path" character varying(500),
  "upload_status" smallint,
  "message" text,
  "create_by" bigint,
  "create_time" timestamp without time zone,
  "update_time" timestamp without time zone,
  "clean_flag" character(1)
);

-- Column comments:
--   id: 主键ID
--   cache_id: 缓存ID：与离线同步任务的cacheId对应，用于批量文件管理
--   file_md5: 文件标识：MD5值，用于唯一标识文件和完整性校验
--   file_type: 文件类型：json-JSON数据文件，image-图片文件
--   file_name: 文件名
--   file_size: 文件总大小：字节
--   uploaded_size: 已上传大小：字节
--   total_chunks: 总分块数
--   uploaded_chunks: 已上传分块列表：JSON数组，记录已完成的分块序号
--   file_path: 文件存储路径：上传完成后的完整路径
--   upload_status: 上传状态：0-待上传，1-上传中，2-上传完成，3-合并失败
--   message: 执行信息：错误日志
--   create_by: 创建人
--   create_time: 创建时间
--   update_time: 更新时间
--   clean_flag: 本地文件清理标记：0 未删除、1 已删除

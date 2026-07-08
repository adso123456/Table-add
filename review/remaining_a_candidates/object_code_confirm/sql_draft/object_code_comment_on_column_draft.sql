-- DRAFT ONLY
-- 本文件仅为 object_code 人工确认后的 COMMENT ON COLUMN SQL 草案，尚未执行。
-- 来源：object_code_confirm_decision_template.csv
-- 生成时间：2026-07-07
-- 禁止未经最终执行前确认直接在生产库执行。
-- ============================================================================
-- #: wst_trace_topology_issue.object_code
-- Human confirmed: 人工确认：object_code 表示监控对象编码；样本 rs_outlet_*/FA-*/HBYC* 符合业务预期
COMMENT ON COLUMN public."wst_trace_topology_issue"."object_code" IS '监控对象编码';

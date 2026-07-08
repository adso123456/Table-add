# COMMENT ON COLUMN Execution Commands Draft

**Generated**: 2026-07-07 15:53:29
**Target**: gt_monitor (localhost:5433)

---

## IMPORTANT

**This file provides command drafts only. No commands were executed at this stage.**

Before execution:
1. Review `pre_execution_checklist.md` and confirm all 13 are ready
2. Review each COMMENT text manually
3. Test in a non-production environment first if possible
4. Back up or confirm rollback path (COMMENT ON can be rolled back by setting to NULL)

---

## Method 1: PowerShell + Local psql

Requires PostgreSQL client tools (psql in PATH).

```powershell
psql "postgresql://postgres:test123456@localhost:5433/gt_monitor" -f "E:\3\code\metadata_audit\review\sql_draft\approved_comment_on_columns_draft.sql"
```

## Method 2: Docker Container

```powershell
Get-Content "E:\3\code\metadata_audit\review\sql_draft\approved_comment_on_columns_draft.sql" | docker exec -i local-timescale psql -U postgres -d gt_monitor
```

## Method 3: Docker Interactive (one-by-one)

```powershell
docker exec -it local-timescale psql -U postgres -d gt_monitor
```

Then paste each COMMENT ON statement one at a time from the SQL draft file.

---

## Post-Execution Verification

### 1. Re-run Metadata Audit

```powershell
& "E:\3\posgresql\1\vanna_venv\Scripts\python.exe" "E:\3\code\metadata_audit\run_metadata_audit.py"
```

### 2. Expected Changes

| Metric | Before | Expected After |
|------|--------|-----------|
| Total tables | 162 | 162 (unchanged) |
| Total columns | 3,445 | 3,445 (unchanged) |
| Columns with comments | 2,846 | **2,859** (+13) |
| Columns missing comments | 599 | **586** (-13) |
| Column comment coverage | 82.6% | **83.0%** |

### 3. Confirm These Disappear from Fill Candidates

After re-running the audit, the following 13 should no longer appear in `comment_fill_candidates.csv`:

| Table | Column |
|-----|------|
| layer_outlet_sewage | jcdbh |
| stg_sjtysj_cbwrwxtzlxxxt_b_day_receive_ship_kpi_df | day |
| wm_hydrological_info | build_time |
| wm_meteorological_info | build_time |
| wm_station_info | build_time |
| wm_waterbody_info | img_name |
| wst_asset_trace_snap | network_type |
| wst_layer_river | created_at |
| wst_layer_river | updated_at |
| wst_trace_topology_issue | created_by |
| wst_trace_topology_issue | created_at |
| wst_trace_topology_issue | updated_by |
| wst_trace_topology_issue | updated_at |

---

## Rollback

To rollback, set the comment to NULL:

```sql
COMMENT ON COLUMN public."table_name"."column_name" IS NULL;
```

---

## Notes

1. COMMENT ON COLUMN is a lightweight DDL - no table lock, no data impact
2. All 13 are low-risk candidates
3. Execute during low-traffic period if possible
4. Re-run audit script after execution to verify coverage change

---

**This file provides command drafts only. No commands were executed at this stage.**

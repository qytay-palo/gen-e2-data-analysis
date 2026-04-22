# Story 02: Sector Breakdown Tab and Smoke Test

## User Story
As a Workforce Planner, I want a Sector Breakdown tab on the dashboard and a smoke test that confirms the app is healthy, so that planners can explore headcount distribution across public and private sectors and I can trust the app before a demo.

## Acceptance Criteria
1. Tab 2 "Sector Breakdown" displays a stacked bar chart with sectors on the x-axis, count on the y-axis, and one colour per profession
2. Year-range slider and profession multi-select filter both update the chart immediately on change
3. Smoke test script at `artifacts/ps-002-workforce-trends-dashboard/tests/integration/test_smoke.py` starts the app, hits `http://localhost:8050`, and asserts HTTP 200
4. Both tabs are visible and functional in the same running app instance

## Technical Notes
- Tab module at `artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/tabs/sector_breakdown.py`
- Appended to tab list in main app file — same pattern as Story 01
- Smoke test uses `subprocess` to start the app and `requests` to hit the endpoint; cleans up the process on exit

## Definition of Done
- Sector Breakdown tab renders with correct stacked bar data
- Smoke test passes (`pytest tests/integration/test_smoke.py`)
- Both tabs visible in the running app with no console errors

## Story Points
3

## Priority
Must Have

## Dependencies
- PS-002 Story 01 complete — app scaffold and tab list must exist

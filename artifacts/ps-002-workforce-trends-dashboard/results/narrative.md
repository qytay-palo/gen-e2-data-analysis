## Executive Summary

PS-002 built the first interactive dashboard layer on top of the PS-001 workforce data foundation: a Plotly Dash app that lets MOH workforce planners explore historical headcount trends without manual preprocessing. In both Demo 1 and Demo 2, this app serves as the opening state shown to stakeholders before any live generation or downstream extensions are introduced.

## Dashboard Features

- **Headcount Over Time**: line chart showing workforce headcount by profession across years, with a year-range slider and a multi-select profession filter.
- **Sector Breakdown**: stacked bar chart showing headcount by profession and sector, with a year-range slider and a multi-select profession filter.
- **Interactive behavior**: both tabs update instantly in-place when filters change, so planners can compare professions and time windows without page reloads.

## How to Run

`python artifacts/ps-002-workforce-trends-dashboard/reports/dashboards/workforce_trends_dashboard.py`

## Extensibility

The app is structured around a shared `TABS` list, so PS-003 and PS-005 can append new `dcc.Tab` modules at runtime instead of rewriting the core app shell. That keeps PS-002 as the stable base experience while allowing growth analysis and forecast integration to land as additional tabs.

## Downstream Value

For Demo 1, this dashboard provides the client-ready opening state that proves the cleaned PS-001 dataset is already usable for self-service exploration. For Demo 2, the same opening state becomes the baseline that PS-005 extends, allowing forecast and narrative-driven views to be added without disrupting the initial trend dashboard experience.
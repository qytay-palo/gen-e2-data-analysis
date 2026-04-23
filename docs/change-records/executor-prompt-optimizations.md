# Change Record: Executor Prompt Optimizations

**Branch**: `demo-add-tab-fast`  
**File changed**: `.github/prompts/2-execution-stage.md`

---

## Summary

Four changes to the execution-stage prompt that together reduced PS-003 runtime from ~20 minutes to ~9 minutes 19 seconds — a 53% reduction.

---

## Changes

### 1. Pre-flight phase skip assessment

**What changed**: Added a pre-flight table that the executor evaluates once — before invoking any agent — to decide which phases are N/A for the current problem statement.

**Why**: PS-003 was invoking six agents that had nothing to do: data-extractor, data-validation, data-cleaning, exploratory-analysis, feature-engineering, and narrative-compiler. The problem statement already contains enough information to determine up-front which phases are needed (inputs section, user stories directory, outputs section). By evaluating this before any agent is spawned, those six cold-starts are avoided entirely.

---

### 2. Clearer Master Trigger Checklist with per-row skip conditions

**What changed**: Split Phase 3 into two independently skippable rows (3a and 3b). Added a Skip condition column showing the exact pre-flight rule that controls each row. Changed checkbox values from `☐ / N/A` to `N/A or ☐` (N/A shown first, making the skipped state the primary signal rather than an afterthought). Completion now marked as `✅`.

**Why**: With only `☐` checkboxes, there was no way to distinguish "not yet run" from "intentionally skipped." Exploratory-analysis and feature-engineering were also bundled into a single row despite being independently applicable — a PS can need one without the other.

---

### 3. Combined quality + review verification per phase

**What changed**: Replaced the two separate subagent calls after each phase (code-quality followed by code-reviewer) with a single combined call — one `code-quality` subagent instructed to also perform a code review pass.

**Why**: Both verification agents were inspecting the same outputs with substantially overlapping concerns. Running them sequentially doubled the verification cost with no meaningful gain in coverage. A single combined pass achieves the same result at half the subagent overhead.

---

### 4. Decision gates added to Phase 3 and Phase 5 prose

**What changed**: Added an explicit decision gate at the top of Phase 3 ("skip entirely if both 3a and 3b are N/A") and Phase 5 ("skip if pre-flight marked it N/A"). Prefixed the feature-engineering agent entry with *(skip if marked N/A in Pre-flight)*.

**Why**: Even after the pre-flight table marked rows N/A, the phase descriptions still read unconditionally ("TRIGGER NOW"). Without a gate in the prose, an executor following the instructions literally could still invoke agents for skipped phases. The gate reinforces the skip decision at the exact moment the executor is about to act.

---

## Applicability to other problem statements

### PS-004 (Headcount Forecasting)

| Pre-flight rule | Outcome |
|-----------------|---------|
| Inputs = `workforce_clean.parquet` (pre-existing) | Phases 1 + 2 skip |
| No `*eda*` / `*exploratory*` user story | Phase 3a skips |
| `01-feature-engineering-and-linear-baseline.md` exists | Phase 3b **runs** |
| `02-train-arima-models.md` + `03-evaluate-select-champion-and-forecast.md` exist | Phase 4 **runs** |
| Outputs are CSVs and `.pkl` files — no written report | Phase 5 skips |

**Net saving**: 3 phases skipped (~6 subagent calls, ~8 min). Phases 3b, 4, and 6 still run in full. The combined verify change also halves the remaining verification overhead.

### PS-005 (Forecast Dashboard Integration)

| Pre-flight rule | Outcome |
|-----------------|---------|
| Inputs = PS-004 CSVs (pre-existing) | Phases 1 + 2 skip |
| No EDA, feature-engineering, or forecasting user story | Phases 3a, 3b, 4 skip |
| Outputs are a tab module + dashboard patch — no written report | Phase 5 skips |

**Net saving**: Identical reduction to PS-003 — only Phase 6 (dashboard-visualization) and one verify call run. PS-005 would have hit the same ~20 min problem for exactly the same reason as PS-003.

---

## General applicability

The changes are most valuable for **downstream PSes** — any PS whose inputs are outputs from a prior PS. This is the common pattern in a multi-PS pipeline: only the first PS in a chain (PS-001 here) legitimately needs phases 1 and 2. The pre-flight rules capture this structurally without any per-PS configuration.

The combined verify change applies universally — every PS was paying the double-verification tax under the old prompt regardless of complexity.

**Where the changes have no effect**:
- **PS-001** (workforce data foundation) genuinely needs extraction, validation, and cleaning since it sources raw SharePoint data. All phases run, and the pre-flight rules correctly leave it untouched.
- Any future PS with a written narrative or findings document as a deliverable — Phase 5 stays in for those.

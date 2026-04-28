# Change Record: Agentic Flow Optimisation

**Branch**: `optimise-agentic-flow`  
**Date**: 2026-04-28  
**Status**: In progress

---

## Background

The execution time for a full PS run was unacceptably long (~20 min for PS-003, estimated ~20 min for PS-005). A partial fix was applied on `demo-add-tab-fast` (see `executor-prompt-optimizations.md`), reducing PS-003 to ~16 min. That fix was scoped to the demo and was not a proper overhaul — it left several structural problems in place.

This change record covers the full overhaul targeting six identified issues. The four-step methodology (project init → problem statements → planning → execution) is **fixed and not subject to change**.

---

## Issues and Changes

### Issue 1 — Inconsistent Naming Convention

**Problem**: PS folders use `PS-001-name`, but user story folders use `problem-statement-001-name` and story files have no entity prefix (`01-extract-*.md`). This makes the relationship between artefacts ambiguous and breaks automation that pattern-matches on paths.

**Change**:
- All PS folders: `PS-001-workforce-data-foundation` (already correct in `artifacts/`)
- User story folders: renamed from `problem-statement-{NNN}-{name}` → `PS-{NNN}-{name}`
- User story files: renamed from `{NN}-{slug}.md` → `US-{NNN}-{slug}.md`
- Implementation plan files (new): `IP-{NNN}-{slug}.md`

**Files changed**: `generate-user-stories.agent.md`, `generate-implementation-plan.agent.md`, `1-planning-stage.md`, `2-execution-stage.md`

---

### Issue 2 — Messy Folder Structure

**Problem**: Agent handoffs are stored under `docs/agent-handoffs/{phase-name}/ps-{num}-{name}/` — double nesting with an inconsistent PS prefix. This makes path resolution in prompts brittle and hard to read.

**Change**: Flatten handoff paths to `docs/agent-handoffs/PS-{NNN}-{name}/{agent-type}-handoff.json`. One folder per PS, one file per agent. No per-phase subfolder.

**Files changed**: All agent `.agent.md` files (handoff output/input path references), `2-execution-stage.md`

---

### Issue 3 — Implementation Plans Embedded in User Story Files

**Problem**: `generate-implementation-plan.agent.md` appends the full implementation plan to the user story file. This bloats story files (which should be short and reusable), makes them hard to diff, and mixes the "what" (user story) with the "how" (implementation plan).

**Change**: Implementation plans written to a separate file `docs/objectives/implementation_plans/PS-{NNN}-{name}/IP-{NNN}-{slug}.md`. User story files remain lean (story, acceptance criteria, DoD only).

**Files changed**: `generate-implementation-plan.agent.md` (remove append rule, add new output path), `1-planning-stage.md` (reference new path)

---

### Issue 4 — Auditability Not Configurable (Notebooks vs Scripts)

**Problem**: Agents unconditionally produce Jupyter notebooks. For demos and production, only Python scripts are needed. Notebook generation wastes time and creates verification overhead (notebook size/cell count checks) that is irrelevant when scripts are the target output.

**Change**: Add an `artifact_format` question to `0-start-gen-e2-data-analysis-project.prompt.md`. Valid values: `scripts`, `notebooks`, `both`. The answer is saved to `docs/project-context/project-settings.yml`. The executor reads this setting in pre-flight and passes the constraint to every subagent. Notebook verification checks are skipped when `artifact_format: scripts`.

**Files changed**: `0-start-gen-e2-data-analysis-project.prompt.md`, `2-execution-stage.md`

---

### Issue 5 — Project Initialisation Answers Not Auditable

**Problem**: All answers provided during `0-start` (business objective, platform, stakeholders, artifact format) exist only in the conversation history. Re-running the project produces different results if the conversation is not preserved. There is no single source of truth.

**Change**: At the end of `0-start`, save all answers to `docs/project-context/project-settings.yml`:

```yaml
project_name: ""
business_objective: ""
success_metrics: ""
platform: ""            # local | databricks | cdsw
stakeholders: []
artifact_format: ""     # scripts | notebooks | both
created_date: ""
```

Steps 1–4 read this file rather than re-asking. Replaying the project means checking out the branch and re-running prompts — the settings are already recorded and deterministic.

**Files changed**: `0-start-gen-e2-data-analysis-project.prompt.md`

---

### Issue 6 — Execution Stage Gating Redesign

**Problem**: The phase list in `2-execution-stage.md` is hardcoded (phases 1, 2, 3a, 3b, 4, 5, 6). The 3a/3b split is non-sequential. Skip logic was added as patches on top of a design originally built to run everything. This is fragile, hard to read, and requires manual maintenance whenever the PS structure changes.

**Change**: Replace the hardcoded phase list with dynamic phase resolution. Pre-flight scans `docs/objectives/user_stories/PS-{NNN}-{name}/` and maps each `US-*.md` filename to the agent that handles it, using a stable filename-pattern → agent mapping:

| US filename pattern | Agent |
|---|---|
| `US-*-extract-*` | `data-extractor` |
| `US-*-validate-*` | `data-validation` |
| `US-*-clean-*` | `data-cleaning` |
| `US-*-explore-*` / `US-*-eda-*` | `exploratory-analysis` |
| `US-*-feature-*` / `US-*-engineer-*` | `feature-engineering` |
| `US-*-forecast-*` / `US-*-model-*` | `model-forecasting` |
| `US-*-narrative-*` / `US-*-report-*` | `narrative-compiler` |
| `US-*-dashboard-*` / `US-*-tab-*` | `dashboard-visualization` |

The executor builds a numbered execution plan from this scan (1, 2, 3... sequentially). Dependency ordering between agents is encoded once as a static sort order, not duplicated across phase descriptions. A PS with one user story produces a one-phase plan.

**Files changed**: `2-execution-stage.md` (full redesign of phase resolution and checklist sections), `executor.agent.md`

---

## Implementation Steps

1. **Rename conventions** — update all path references in agent files and prompt files to use `PS-{NNN}` / `US-{NNN}` / `IP-{NNN}` prefixes
2. **Flatten handoff paths** — update all `docs/agent-handoffs/` references from `{phase}/{ps}/` to `PS-{NNN}/{agent}-handoff.json`
3. **Separate implementation plans** — update `generate-implementation-plan.agent.md` output target and `1-planning-stage.md` validation reference
4. **Add auditability toggle** — add question + `project-settings.yml` write to `0-start`, add settings read + notebook skip logic to `2-execution-stage.md`
5. **Persist 0-start answers** — extend `0-start` to write all answers to `project-settings.yml`
6. **Redesign execution gating** — replace hardcoded phase list in `2-execution-stage.md` with dynamic phase resolution; update `executor.agent.md` to match

---

## Expected Outcome

| Metric | Before | Target |
|---|---|---|
| PS-003 cold-start runtime | ~20 min (pre-demo fix), ~16 min (post-fix) | ~10 min |
| PS-005 cold-start runtime | ~20 min (estimated) | ~5 min (1 US = 1 phase) |
| Subagent calls for PS-005 | ~12 (6 phases × 2 verify) | ~2 (1 phase + 1 verify) |
| Replaying a project deterministically | Not possible | Possible via `project-settings.yml` |
| Notebook overhead when not needed | Always present | Zero when `artifact_format: scripts` |

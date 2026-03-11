```javascript
#runSubagent({
  description: "Comprehensive code review for Problem Statement {num}",
  prompt: `Execute a comprehensive code quality review and fix ALL identified issues.

Context:
- Target Directory: problem-statement/ps-{num}-{descriptive-name}/
- Review ALL Python files (.py) and notebooks (.ipynb)
- Fix issues immediately - do not just report them
- **CRITICAL**: Any errors detected during code execution MUST BE FIXED before proceeding

**Tasks:**
1. **Directory Structure and Import Path Consistency:** Run `ruff format problem-statement/ps-{num}-{descriptive-name}/ --check`
   - Auto-format code if needed

2. **Execute All Code to Verify No Runtime Errors:** Run all Python scripts and notebooks once to ensure they execute without errors, and resolve any errors found
   - **MANDATORY**: All runtime errors, import errors, and execution failures MUST BE FIXED immediately

3. You review code through multiple perspectives simultaneously. Run each perspective as a **parallel** subagent so findings are independent and unbiased.

When asked to review code, run these subagents in parallel:
- Correctness reviewer: logic errors, edge cases, type issues.
- Code quality reviewer: readability, naming, duplication.
- Security reviewer: input validation, injection risks, data exposure.
- Architecture reviewer: codebase patterns, design consistency, structural alignment.
`
})
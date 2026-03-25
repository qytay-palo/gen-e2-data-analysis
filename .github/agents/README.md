# Agent Templates

This directory contains prompt templates for each specialized agent in the multi-agent data analysis pipeline.

## Template Structure

Each agent template includes:
1. **Role Definition**: What the agent specializes in
2. **Context Variables**: Placeholders for runtime substitution
3. **Instruction References**: Which `.github/instructions/` files to follow
4. **Responsibilities**: Specific tasks to perform
5. **Output Specifications**: Exact files and formats to generate
6. **Handoff Protocol**: How to pass context to next agent
7. **Success Criteria**: Validation gates to pass

## Available Templates

### Core Pipeline Agents
- **extraction.agent.md** - Data extraction and loading (Stage 0-2)
- **profiling.agent.md** - Data quality assessment (Stage 3)
- **cleaning.agent.md** - Data cleaning and preprocessing (Stage 4) *[To be created]*
- **eda.agent.md** - Exploratory data analysis (Stage 5)
- **modeling.agent.md** - Statistical modeling and forecasting (Stage 7) *[To be created]*
- **visualization.agent.md** - Publication-quality visualizations (Stage 9) *[To be created]*

### Code Quality Agents
- **quality.agent.md** - ✅ Comprehensive code quality review (error handling, type safety, security, testing)
- **duplicate_detection.agent.md** - ✅ Identify duplicate code patterns and refactoring opportunities
- **dead_code_elimination.agent.md** - ✅ Find and remove unused imports, functions, and obsolete files
- **eda.agent.md** - ✅ Exploratory data analysis (Stage 5)
- **extraction.agent.md** - ✅ Extract data from various sources and prepare for analysis (Stage 0-2)

### Supporting Agents
- **documentation_agent.md** - Technical documentation (Stage 9) *[To be created]*
- **planning_agent.md** - ✅ Implementation planning and task breakdown

## Template Variables

When using templates, replace these variables:
- `{problem_statement_num}` - Problem statement number (e.g., "001")
- `{problem_statement_title}` - Full problem title
- `{timestamp}` - Format: YYYYMMDD_HHMMSS
- `{data_sources}` - List of data sources
- `{input_data_path}` - Path to input data file
- `{cleaned_data_path}` - Path to cleaned data

### Adaptive Implementation Workflow

**CRITICAL** Each agent follows this workflow to ensure **data-driven and context-aware** implementation:

```

**Stage Execution Workflow (Per Agent)**

1. READ CONTEXT
   ├─ Load implementation plan segment for this stage
   ├─ Read agent template (.github/agents/{agent}.agent.md)
   └─ Read stage instructions (.github/instructions/data-analysis-stages-instructions/)

2. VALIDATE INPUTS (from previous stage)
   ├─ Read handoff file from previous agent
   ├─ Verify all input files exist
   ├─ Validate data schema and quality gates
   └─ Review recommended actions from previous stage

3. GATHER ADDITIONAL CONTEXT (if needed)
   ├─ Use MCP filesystem tools to inspect data
   ├─ Use Context7 to fetch library documentation
   ├─ Query existing codebase patterns
   └─ Review configuration files

4. IMPLEMENT STAGE REQUIREMENTS
   ├─ Generate code following project best practices
   ├─ Apply recommended actions from previous stage
   ├─ Create notebooks for user visibility
   └─ Generate all required outputs

5. VALIDATE OUTPUTS
   ├─ Execute all generated code (Python scripts AND notebooks)
   ├─ Verify zero execution errors
   ├─ Check output files exist and are valid
   └─ Validate against stage-specific success criteria

6. CREATE HANDOFF
   ├─ Generate handoff file for next agent
   ├─ Document findings and recommendations
   ├─ Set validation_status based on success criteria
   └─ Specify recommended next steps

7. QUALITY CHECK (before proceeding)
   ├─ Run code review subagent
   ├─ Execute notebook validation subagent
   ├─ Fix any critical issues found
   └─ Re-validate until all quality gates pass

8. PROCEED TO NEXT STAGE
   └─ Hand off to next agent via handoff file
```

## Usage Example

```python
# orchestrator.py
def load_agent_template(agent_name: str, context: dict) -> str:
    """Load and populate agent template with context."""
    template_path = f".agents/templates/{agent_name}.md"
    
    with open(template_path) as f:
        template = f.read()
    
    # Replace variables
    for key, value in context.items():
        template = template.replace(f"{{{key}}}", str(value))
    
    return template

# Usage
context = {
    "problem_statement_num": "001",
    "problem_statement_title": "Workforce Capacity Mismatch",
    "timestamp": "20260223_141530",
    "data_sources": "Kaggle: healthcare-capacity-sg"
}

extraction_prompt = load_agent_template("extraction_agent", context)
```

## Creating New Templates

When creating a new agent template:
1. Copy structure from existing template
2. Define clear role and scope
3. Reference appropriate instruction files
4. Specify exact output files and formats
5. Define handoff protocol
6. Include validation criteria
7. Document common issues and solutions

## Handoff Protocol

All agents must create handoff files in:
```
data/3_interim/agent_handoffs/{source_agent}_to_{target_agent}_{timestamp}.json
```

Standard handoff schema:
```json
{
  "agent_name": "SourceAgent",
  "timestamp": "YYYYMMDD_HHMMSS",
  "stage": 3,
  "problem_statement": "001",
  "outputs": {...},
  "validation_status": "passed|failed",
  "findings": {...},
  "recommended_next_step": "next_agent_name"
}
```

## See Also
- [Agent Registry](../.agents/registry.yml) - Agent capabilities and mappings
- [Orchestration Config](../.agents/config.yml) - Pipeline configuration
- [Stage Instructions](../.github/instructions/data-analysis-stages-instructions/) - Detailed stage guidance

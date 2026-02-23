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
- **extraction_agent.md** - Data extraction and loading (Stage 0-2)
- **profiling_agent.md** - Data quality assessment (Stage 3)
- **cleaning_agent.md** - Data cleaning and preprocessing (Stage 4) *[To be created]*
- **eda_agent.md** - Exploratory data analysis (Stage 5)
- **modeling_agent.md** - Statistical modeling and forecasting (Stage 7) *[To be created]*
- **visualization_agent.md** - Publication-quality visualizations (Stage 9) *[To be created]*

### Supporting Agents
- **quality_agent.md** - Code quality and testing (Stage 8, 10) *[To be created]*
- **documentation_agent.md** - Technical documentation (Stage 9) *[To be created]*

## Template Variables

When using templates, replace these variables:
- `{problem_statement_num}` - Problem statement number (e.g., "001")
- `{problem_statement_title}` - Full problem title
- `{timestamp}` - Format: YYYYMMDD_HHMMSS
- `{data_sources}` - List of data sources
- `{input_data_path}` - Path to input data file
- `{cleaned_data_path}` - Path to cleaned data

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

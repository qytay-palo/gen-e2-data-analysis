# Multi-Agent Data Analysis Workspace

This workspace is configured for multi-agent collaborative data analysis workflows.

## 🎯 Quick Start

### Running a Full Analysis Pipeline

```bash
# Run sequential pipeline for a problem statement
python src/orchestration/pipeline_orchestrator.py \
    --problem-statement 001 \
    --pipeline-type sequential \
    --agents extraction,profiling,cleaning,eda,modeling,visualization

# Check orchestration logs
tail -f logs/orchestration/orchestrator_*.log
```

### Agent-Specific Execution

```bash
# Run single agent (for debugging)
python scripts/run_agent.py --agent profiling --problem-statement 001

# Run parallel EDA tasks
python scripts/run_agent.py --agent eda --parallel univariate,temporal,spatial
```

## 📁 Multi-Agent Structure

```
.agents/
├── config.yml              # Orchestration configuration
├── registry.yml            # Agent capabilities and mappings
├── skills/                 # Domain-specific knowledge
│   ├── moh-data-quality-assessment/
│   └── README.md
└── templates/              # Agent prompt templates
    ├── extraction_agent.md
    ├── profiling_agent.md
    ├── eda_agent.md
    └── README.md

data/3_interim/agent_handoffs/  # Inter-agent communication
src/orchestration/              # Pipeline orchestration utilities
```

## 🚀 Analysis Workflow

### Stage-Based Pipeline
```
ExtractionAgent → ProfilingAgent → CleaningAgent → EDAAgent → ModelingAgent → VisualizationAgent
                                                                                    ↓
                                                                            DocumentationAgent
                                                                                    ↓
                                                                              QualityAgent
```

### Handoff Protocol
Each agent creates a handoff file with:
- Outputs (code, data, figures)
- Validation status (passed/warning/failed)
- Key findings
- Recommended next step

Example handoff: `data/3_interim/agent_handoffs/profiling_to_cleaning_20260223_141530.json`

## 📋 Configuration

### Pipeline Types
- **Sequential**: Agents run one after another (default)
- **Parallel**: Independent tasks run concurrently (EDA sections, multiple forecasts)
- **Adaptive**: Pipeline adjusts based on data quality findings

Configure in [`.agents/config.yml`](.agents/config.yml):
```yaml
orchestrator:
  pipeline_type: sequential  # or parallel, adaptive
  verification_mode: strict
```

### Adding New Agents
1. Create template in `.agents/templates/{agent_name}.md`
2. Register in `.agents/registry.yml`
3. Add configuration in `.agents/config.yml`
4. Update orchestrator if needed

## 🔧 Development

### Creating Domain Skills
```bash
# Create new skill directory
mkdir -p .agents/skills/new-skill-name

# Create SKILL.md with template
cat > .agents/skills/new-skill-name/SKILL.md <<EOF
---
name: new-skill-name
description: Brief description
version: 1.0.0
applies_to: [AgentName]
tags: [domain, topic]
---
# Skill content here
EOF

# Register in .agents/registry.yml
```

### Testing Agent Execution
```bash
# Unit tests for orchestration
pytest tests/unit/test_orchestration.py

# Integration test for full pipeline
pytest tests/integration/test_pipeline.py
```

## 📊 Monitoring

### Pipeline Execution Logs
```bash
# View orchestration logs
ls logs/orchestration/

# View agent-specific logs
ls logs/etl/            # Extraction, profiling, cleaning
ls logs/audit/          # Quality checks
ls logs/errors/         # Error tracking
```

### Handoff History
```bash
# View all handoffs for a problem statement
ls data/3_interim/agent_handoffs/*_to_*_*.json

# Validate handoff files
python scripts/validate_handoffs.py --problem-statement 001
```

## 🎓 Learning Resources

- [Multi-Agent Config Documentation](.agents/config.yml)
- [Agent Registry](.agents/registry.yml)
- [Handoff Protocol](data/3_interim/agent_handoffs/README.md)
- [Agent Templates](.agents/templates/README.md)
- [Domain Skills](.agents/skills/README.md)
- [Orchestration Guide](src/orchestration/README.md)

## 🔗 Integration Points

### GitHub Copilot
- Copilot instructions reference agent templates
- Stage-specific instructions linked to agents
- See [`.github/copilot-instructions.md`](.github/copilot-instructions.md)

### Databricks
- Agents can execute on Databricks clusters
- Configure cluster settings in `config/databricks.yml`
- Use `databricks-connect` for remote execution

### MCP Tools
- Agents use MCP filesystem tools for file operations
- Configured in `.cline/mcp_settings.json`
- Supports parallel file operations

## 📈 Expected Benefits

| Aspect | Single Agent | Multi-Agent |
|--------|-------------|-------------|
| **Speed** | Sequential | Parallel where possible |
| **Expertise** | Generalist | Specialist per stage |
| **Quality** | Single review | Multiple validation layers |
| **Debugging** | Monolithic | Clear stage boundaries |
| **Reusability** | Code duplication | Shared skills library |

## 🔍 Troubleshooting

### Agent Validation Fails
```bash
# Check handoff file for details
cat data/3_interim/agent_handoffs/latest_handoff.json | jq '.findings'

# Review validation criteria
cat .agents/config.yml | grep -A 5 "validation:"
```

### Pipeline Stuck
```bash
# Check which stage failed
tail -n 50 logs/orchestration/orchestrator_*.log

# Restart from specific agent
python src/orchestration/pipeline_orchestrator.py \
    --resume-from cleaning \
    --problem-statement 001
```

## 📞 Support

- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Documentation: [`docs/`](docs/)
- Stage Instructions: [`.github/instructions/data-analysis-stages-instructions/`](.github/instructions/data-analysis-stages-instructions/)

---

**Last Updated**: 2026-02-23
**Orchestration Version**: 1.0.0

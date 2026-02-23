# Domain-Specific Skills for Multi-Agent System

This directory contains domain-specific knowledge modules that agents can reference during execution.

## Purpose
Skills provide specialized knowledge that goes beyond general coding instructions. They capture:
- Domain-specific procedures (e.g., MOH data validation rules)
- Singapore-specific healthcare context
- Epidemiological calculation methods
- Data source-specific authentication and usage patterns

## Skill Structure

Each skill is organized in its own directory:
```
.agents/skills/
├── skill-name/
│   ├── SKILL.md           # Main skill definition
│   ├── examples/          # Code examples (optional)
│   └── references/        # External references (optional)
```

## Available Skills

### 1. Kaggle Data Extraction
**Path**: `kaggle-data-extraction/SKILL.md`
**Used by**: ExtractionAgent
**Purpose**: Kaggle API authentication, dataset search, download procedures

### 2. Data Quality Assessment
**Path**: `data-quality-assessment/SKILL.md`
**Used by**: ProfilingAgent, CleaningAgent
**Purpose**: MOH data quality standards, validation criteria, scoring methodology

### 3. MOH Data Standards
**Path**: `moh-data-standards/SKILL.md`
**Used by**: CleaningAgent, EDAAgent
**Purpose**: Singapore MOH data formatting, disease classification (ICD-10-SG), reporting standards

### 4. Epidemiological Metrics
**Path**: `epidemiological-metrics/SKILL.md`
**Used by**: EDAAgent, ModelingAgent
**Purpose**: Disease surveillance metrics, incidence/prevalence calculations, seasonality detection

### 5. Seasonal Forecasting
**Path**: `seasonal-forecasting/SKILL.md`
**Used by**: ModelingAgent
**Purpose**: Time series forecasting for seasonal disease patterns, SARIMAX configuration

### 6. MOH Presentation Standards
**Path**: `moh-presentation-standards/SKILL.md`
**Used by**: VisualizationAgent, DocumentationAgent
**Purpose**: MOH reporting standards, color schemes, chart formatting guidelines

## Creating a New Skill

1. **Create directory structure**:
   ```bash
   mkdir -p .agents/skills/new-skill-name
   ```

2. **Create SKILL.md** with this template:
   ```markdown
   ---
   name: skill-name
   description: What this skill provides and when to use it
   version: 1.0.0
   applies_to: [AgentName1, AgentName2]
   tags: [domain, healthcare, singapore]
   ---
   
   # Skill Name
   
   ## Overview
   Brief description of what specialized knowledge this skill provides.
   
   ## When to Use
   Specific scenarios where agents should reference this skill.
   
   ## Procedures
   Step-by-step procedures, algorithms, or workflows.
   
   ## Examples
   Code examples or usage patterns.
   
   ## References
   External documentation, standards, or research papers.
   ```

3. **Register in registry.yml**:
   ```yaml
   skills_library:
     - name: new-skill-name
       path: .agents/skills/new-skill-name/SKILL.md
       applies_to: [AgentName1, AgentName2]
       description: Brief description
   ```

## Skill vs Instruction File

| Aspect | Skill | Instruction File |
|--------|-------|------------------|
| **Scope** | Domain-specific knowledge | General coding/analysis best practices |
| **Audience** | Specific agents | All developers/agents |
| **Content** | Procedures, domain rules, calculations | Standards, conventions, workflows |
| **Location** | `.agents/skills/` | `.github/instructions/` |
| **Example** | "How to calculate disease incidence rate" | "How to write clean Python code" |

## Best Practices

1. **Keep skills focused**: One skill = one domain concept
2. **Include examples**: Show actual code or calculations
3. **Reference standards**: Link to MOH guidelines, ICD-10-SG, etc.
4. **Version skills**: Update version when procedures change
5. **Tag appropriately**: Use tags for discoverability

## Maintenance

- Review skills quarterly for accuracy
- Update when MOH standards change
- Retire obsolete skills (move to `archive/`)
- Keep examples up-to-date with latest Python/Polars versions

## See Also
- [Agent Registry](../.agents/registry.yml) - Maps skills to agents
- [Domain Knowledge](../docs/domain_knowledge/) - Background information
- [MOH Guidelines](https://www.moh.gov.sg) - Official standards

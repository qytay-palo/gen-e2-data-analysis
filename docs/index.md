# Gen-E2 Data Analysis - Documentation Index

**Welcome to the Gen-E2 Data Analysis Project Documentation**

This project analyzes temporal patterns across infectious diseases in Singapore to identify seasonal trends and forecast outbreak periods. It also prioritizes resource allocation based on disease burden.

---

## 🎯 Start Here

### New to the Project?
1. Read [../README.md](../README.md) for project overview and setup
2. Review [Project Objectives](#project-objectives) below
3. Check [Data Sources](project_context/data-sources.md) for available data
4. Read relevant [Problem Statements](#problem-statements)

### Looking for Something Specific?
- **Data Schemas**: See [Data Dictionary](#data-dictionary)
- **Analysis Methods**: See [Methodology](#methodology)
- **Tech Stack**: See [Technical Context](#technical-context)
- **Tasks & Progress**: See [../TODO.md](../TODO.md)

### Technical Environment
- **Platform**: HEALIX / Databricks
- **Data Volume**: 434 KB
- **Stakeholders**: Minister of Health, internal committee members

---

## 📂 Documentation Structure

### 1. Project Objectives

Central definitions of what we're trying to achieve and why it matters.

#### Problem Statements
Detailed problem definitions with research questions, success metrics, and scope.

- **[Problem Statement Portfolio Index](objectives/problem_statements/README.md)** - Overview and prioritization
- **[PS-001: Seasonal Pattern Forecasting](objectives/problem_statements/ps-001-seasonal-pattern-forecasting.md)** ⭐ CRITICAL
  - Which diseases show strong seasonality?
  - Can we forecast high-risk periods for Dengue, HFMD, Influenza?
  - Deliverables: Seasonality report, 6-month forecasts, risk calendar

- **[PS-002: Disease Burden Prioritization](objectives/problem_statements/ps-002-disease-burden-prioritization.md)** ⭐ HIGH
  - What are top contributors to disease burden?
  - How should resources be allocated across prevention programs?
  - Deliverables: Burden ranking, allocation framework, trend analysis

- **[PS-003: Executive Surveillance Dashboard](objectives/problem_statements/ps-003-executive-surveillance-dashboard.md)** 🟡 MEDIUM
  - Consolidate disease intelligence for executive decision-making
  - Enable self-service exploration of trends and forecasts
  - Deliverables: Interactive Streamlit dashboard, user guide, automated refresh pipeline

#### User Stories
Data analysis lifecycle decomposition of problem statements into actionable increments.

- **[PS-001 User Stories](objectives/user_stories/problem-statement-001-seasonal-forecasting/index.md)** - 8 stories across data extraction through stakeholder reporting
- **[PS-002 User Stories](objectives/user_stories/problem-statement-002-disease-burden/index.md)** - 4 stories focused on burden metrics and resource allocation
- **[PS-003 User Stories](objectives/user_stories/problem-statement-003-executive-dashboard/index.md)** - 6 stories covering dashboard design through deployment
Stakeholder-specific requirements and acceptance criteria.

- [PS-001: Seasonal Forecasting User Stories](objectives/user_stories/ps-001-seasonal-forecasting-user-stories.md) *(To be created)*
- [PS-002: Disease Burden User Stories](objectives/user_stories/ps-002-disease-burden-user-stories.md) *(To be created)*

---

### 2. Data Dictionary

Comprehensive reference for all datasets, fields, and data lineage.

- **[Master Data Index](data_dictionary/README.md)** *(To be created)*
  - Links to individual data domain dictionaries
  - Data quality notes and known limitations

#### Domain-Specific Dictionaries
- [Infectious Disease Data](data_dictionary/infectious-diseases-data-dictionary.md) *(To be created)*
- [Healthcare Workforce Data](data_dictionary/healthcare-workforce-data-dictionary.md) *(To be created)*
- [Healthcare Facilities Data](data_dictionary/healthcare-facilities-data-dictionary.md) *(To be created)*

---

### 3. Methodology

Statistical methods, frameworks, and analytical approaches.

- **[Statistical Methods Overview](methodology/statistical-methods.md)** *(To be created)*
  - Time series analysis techniques
  - Forecasting model selection
  - Seasonality detection methods
  - Burden metric calculations

- **[Implementation Plans](methodology/)**
  - [PS-001 Implementation Plan](methodology/ps-001-implementation-plan.md) *(To be created)*
  - [PS-002 Implementation Plan](methodology/ps-002-implementation-plan.md) *(To be created)*

- **[Data Quality Framework](methodology/data-quality-framework.md)** *(To be created)*
  - Validation rules and thresholds
  - Missing data handling strategies
  - Outlier detection methods

---

### 4. Technical Context

Information about platforms, tools, and data sources.

- **[Business Objectives](project_context/business-objectives.md)**
  - MOH mission and strategic goals
  - Current healthcare challenges
  - Analysis focus areas

- **[Data Sources](project_context/data-sources.md)**
  - Kaggle Health Dataset details
  - Data access methods
  - Available tables and coverage

- **[Tech Stack](project_context/tech-stack.md)**
  - HEALIX/Databricks platform specs
  - Approved libraries and tools
  - Development environment setup

---

## 🔍 Quick Reference

### Common Tasks

| Task | Documentation |
|------|---------------|
| Understand project goals | [Business Objectives](project_context/business-objectives.md) |
| Set up development environment | [../README.md](../README.md) |
| Access data | [Data Sources](project_context/data-sources.md) |
| Understand a specific dataset | [Data Dictionary](data_dictionary/) |
| Learn analysis methodology | [Methodology](methodology/) |
| Find analysis parameters | [../config/analysis.yml](../config/analysis.yml) |
| Check Databricks settings | [../config/databricks.yml](../config/databricks.yml) |

### Stakeholder-Specific Guides

#### For Analysts
1. [Problem Statements](objectives/problem_statements/) - Understand research questions
2. [Data Dictionary](data_dictionary/) - Know your data
3. [Methodology](methodology/) - Apply correct methods
4. [Tech Stack](project_context/tech-stack.md) - Use approved tools

#### For Developers
1. [../README.md](../README.md) - Setup and coding standards
2. [../.github/instructions/](../.github/instructions/) - Detailed coding conventions
3. [../config/](../config/) - Configuration files
4. [Data Sources](project_context/data-sources.md) - Data access patterns

#### For Stakeholders
1. [Business Objectives](project_context/business-objectives.md) - Context and mission
2. [Problem Statements](objectives/problem_statements/) - What we're solving
3. [../TODO.md](../TODO.md) - Progress tracking
4. [../reports/](../reports/) - Analysis deliverables

---

## 📋 Documentation Standards

### When to Create New Documentation

- **Problem Statement**: For each major research question or business decision
- **Data Dictionary**: For each new data source or table added
- **Methodology Document**: For each new statistical technique or framework
- **User Story**: For each stakeholder requirement

### Documentation Format

All documentation should include:
- **Last Updated Date**: Keep current
- **Owner/Author**: Who maintains this
- **Related Documents**: Links to dependencies
- **Status**: Draft, Review, Approved

### Linking Conventions

- Use relative paths: `[Link](../path/to/file.md)`
- Always verify links work after creating
- Update this index when adding new documents

---

## 🔄 Recently Updated

| Document | Last Updated | Change Summary |
|----------|--------------|----------------|
| [Problem Statement Portfolio Index](objectives/problem_statements/README.md) | 2026-02-20 | Validated portfolio against actual data, added PS-003 |
| [PS-001: Seasonal Pattern Forecasting](objectives/problem_statements/ps-001-seasonal-pattern-forecasting.md) | 2026-02-20 | Added metadata, validated data sources |
| [PS-002: Disease Burden Prioritization](objectives/problem_statements/ps-002-disease-burden-prioritization.md) | 2026-02-20 | Added metadata, validated data sources |
| [PS-003: Executive Surveillance Dashboard](objectives/problem_statements/ps-003-executive-surveillance-dashboard.md) | 2026-02-20 | Initial creation |
| [Business Objectives](project_context/business-objectives.md) | 2026-01-30 | Added 2026 focus areas |
| [Data Sources](project_context/data-sources.md) | 2026-01-30 | Documented Kaggle dataset |
| [Tech Stack](project_context/tech-stack.md) | 2026-01-30 | HEALIX/Databricks specs |

---

## 📝 Contributing to Documentation

### Adding New Documents

1. Create document in appropriate folder
2. Follow naming convention: `lowercase-with-hyphens.md`
3. Include standard header (title, date, owner)
4. **Update this index** with link and description
5. Cross-reference related documents

### Documentation Review Process

1. Draft → Author creates initial version
2. Review → Team reviews for accuracy
3. Approved → Stakeholder sign-off
4. Maintain → Keep updated as project evolves

---

## 🔗 External Resources

### MOH Resources
- [MOH Official Website](https://www.moh.gov.sg/)
- [Data.gov.sg](https://data.gov.sg/) - Public health datasets

### Technical Documentation
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [Databricks Documentation](https://docs.databricks.com/)
- [Prophet Documentation](https://facebook.github.io/prophet/)

### Statistical Methods
- [Time Series Analysis (Penn State)](https://online.stat.psu.edu/stat510/)
- [Forecasting: Principles and Practice](https://otexts.com/fpp3/)

---

**Documentation Maintained By**: MOH Analytics Team  
**Last Index Update**: 20 February 2026  
**Next Review**: Monthly (1st of each month)

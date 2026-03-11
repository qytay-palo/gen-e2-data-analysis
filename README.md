# Gen-E2: Singapore Health Trends Analysis

> **Data-driven analysis for policy decision-making in Singapore's healthcare system**

## 📋 Project Overview

This project analyzes health trends in Singapore to support evidence-based policy decisions. The analysis helps stakeholders understand current health patterns, identify areas requiring improvement in the healthcare system, and develop necessary public health policies.

### Business Objectives
- **Primary Goal**: Understand current health trends in Singapore to inform policy making
- **Key Questions**:
  - What health trends require immediate policy intervention?
  - Which sectors or regions of Singapore's health system need improvement?
  - What data-driven predictions can guide future health policies?

### Success Metrics
- Actionable insights derived from analysis
- Reasonable and validated predictions associated with health data
- Evidence-based recommendations for policy makers

### Stakeholders
- **Policy Makers**: Evidence for policy formulation
- **Government Health Officials**: Strategic planning and resource allocation  
- **Team Heads**: Operational decisions and program prioritization

---

## 🏗️ Project Structure

This project uses a **hybrid folder structure** that balances shared infrastructure with problem-specific analyses:

```
gen-e2/
├── shared/                    # ♻️ SHARED INFRASTRUCTURE
│   ├── src/                   # Reusable production code (library functions)
│   │   ├── utils/             # Helper functions, config loaders, loggers
│   │   ├── data_processing/   # ETL functions, cleaning, validation
│   │   ├── analysis/          # Statistical algorithms, trend detection
│   │   ├── models/            # Modeling utilities, evaluation metrics
│   │   ├── visualization/     # Plotting utilities, chart generators
│   │   └── orchestration/     # Multi-agent pipeline orchestration
│   │
│   ├── data/                  # Single source of truth for data
│   │   ├── 1_raw/             # Original immutable source data (READ-ONLY)
│   │   ├── 2_external/        # External reference data
│   │   ├── 3_interim/         # Shared intermediate processing
│   │   └── 4_processed/       # Shared processed datasets
│   │
│   ├── sql/                   # SQL queries and database scripts
│   ├── tests/                 # Tests for shared code
│   └── config/                # Shared configuration files
│
├── problem-statements/        # 📦 SELF-CONTAINED ANALYSES
│   └── ps-{num}-{name}/       # Each problem statement is a complete package
│       ├── README.md          # Problem overview and objectives
│       ├── notebooks/         # Interactive exploratory analysis
│       ├── src/               # Problem-specific code (imports from shared/)
│       ├── data/              # Problem-specific data outputs
│       ├── results/           # Analysis outputs, metrics, exports
│       ├── reports/           # Visualizations, dashboards, presentations
│       ├── models/            # Trained models and artifacts
│       └── config/            # Problem-specific configuration
│
├── docs/                      # 📚 PROJECT DOCUMENTATION
│   ├── index.md               # Central documentation hub
│   ├── objectives/            # Problem statements and user stories
│   ├── data_dictionary/       # Data schemas and definitions
│   ├── methodology/           # Statistical methods and frameworks
│   └── project_context/       # Business objectives, tech stack
│
├── .agents/                   # 🤖 MULTI-AGENT ORCHESTRATION
│   ├── config.yml             # Pipeline orchestration settings
│   ├── registry.yml           # Agent capabilities and mappings
│   ├── templates/             # Agent-specific prompt templates
│   └── skills/                # Domain-specific knowledge modules
│
└── logs/                      # Application logs (ETL, errors, audit)
```

### Key Principles
1. **Shared Resources** (`shared/`): Write once, use everywhere
2. **Problem Isolation** (`problem-statements/`): Self-contained analyses
3. **Import Pattern**: Problem-specific code imports from `shared/src/`
4. **Data Strategy**: Raw data in `shared/data/1_raw/` (single source)

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.9+** (Databricks Runtime 13.3 compatibility)
- **uv** package manager (or pip as fallback)

### 2. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd gen-e2

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env with your credentials
```

### 3. Configure Credentials

Edit `.env` file with your actual credentials:
- **Databricks**: Host, token, cluster ID
- **Database**: Connection details
- **External APIs**: Kaggle, AWS, Azure (if needed)

### 4. Verify Installation

```bash
# Run tests
pytest

# Check Python environment
which python  # Should point to .venv/bin/python

# Verify key packages
python -c "import polars; print(polars.__version__)"
```

---

## 💻 Technology Stack

### Platform
- **Target**: HEALIX/Databricks
- **Runtime**: Databricks 13.3.x (Python 3.9, Spark 3.4)
- **Cluster**: Configured in `shared/config/databricks.yml`

### Core Libraries

| Category | Library | Purpose |
|----------|---------|---------|
| **Data Processing** | Polars (primary) | High-performance DataFrame operations |
| | Pandas (fallback) | When Polars lacks functionality |
| | PySpark | Distributed computing on Databricks |
| **Visualization** | Matplotlib, Seaborn | Statistical visualizations |
| | Plotly, Altair | Interactive dashboards |
| **Analysis** | scikit-learn | Machine learning |
| | statsmodels | Statistical modeling |
| **Utilities** | loguru | Logging (preferred over print) |
| | great-expectations | Data quality validation |
| **Testing** | pytest | Testing framework |

**See**: [`requirements.txt`](requirements.txt) for complete dependencies

---

## 📊 Development Workflow

### Problem-Driven Approach

1. **Define Problem Statement** → `docs/objectives/problem_statements/ps-{num}-{name}.md`
2. **Create Problem Folder** → Use script: `scripts/shared/create_problem_statement.sh`
3. **Data Extraction** → Create connectors in `shared/src/data_processing/`
4. **Exploratory Analysis** → Work in `problem-statements/ps-{num}/notebooks/`
5. **Production Code** → Refactor to `shared/src/` (if reusable) or `ps-{num}/src/` (if specific)
6. **Testing** → Write tests in `shared/tests/` or `ps-{num}/tests/`
7. **Documentation** → Update `docs/` and problem README

### Data Processing Standards

**✅ DO:**
```python
import polars as pl
from loguru import logger

# Lazy loading for large files
df = pl.scan_csv("shared/data/1_raw/disease_data.csv").collect()

# Type-safe transformations
df_clean = (
    df.clone()
    .drop_nulls(subset=['date', 'case_count'])
    .with_columns([
        pl.col('date').str.strptime(pl.Date, '%Y-%m-%d'),
        pl.col('disease').cast(pl.Categorical)
    ])
)

# Logging instead of print
logger.info(f"Processed {len(df_clean)} records")
```

**❌ DON'T:**
```python
# Hardcoded values
diseases = ['Dengue', 'HFMD']  # Use config/base.yml

# Modifying raw data
df.write_csv('shared/data/1_raw/source.csv')  # NEVER!

# Print statements
print("Done")  # Use logger.info() instead
```

---

## 🤖 Multi-Agent System

This project uses specialized agents for complex workflows:

- **ExtractionAgent**: Data loading and extraction
- **ProfilingAgent**: Data quality assessment
- **CleaningAgent**: Data preprocessing
- **EDAAgent**: Exploratory analysis
- **ModelingAgent**: Statistical modeling
- **VisualizationAgent**: Chart generation
- **QualityAgent**: Testing and validation
- **DocumentationAgent**: Technical writing

**Configuration**: See [`.agents/config.yml`](.agents/config.yml)

**Handoff Protocol**: Agents communicate via JSON in `shared/data/3_interim/agent_handoffs/`

---

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| [`shared/config/base.yml`](shared/config/base.yml) | Base settings (data paths, logging, analysis parameters) |
| [`shared/config/databricks.yml`](shared/config/databricks.yml) | Databricks cluster and storage configuration |
| [`.env`](.env.example) | Environment variables (credentials, API keys) |
| [`pytest.ini`](pytest.ini) | Testing configuration |

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests
pytest -m data           # Data validation tests

# Generate coverage report
pytest --cov=shared/src --cov-report=html
```

**Target**: 80%+ code coverage for critical modules

---

## 📁 Key Documentation

- **[Documentation Hub](docs/index.md)**: Complete documentation navigation
- **[Business Objectives](docs/project_context/business-objectives.md)**: Project goals and context
- **[Data Sources](docs/project_context/data-sources.md)**: Available datasets
- **[Tech Stack](docs/project_context/tech-stack.md)**: Approved technologies
- **[TODO Task Tracker](TODO.md)**: Project tasks and ownership

---

## 🔒 Data Security

⚠️ **IMPORTANT**:
- Raw data files (> 10MB) are **not committed** to Git
- Credentials in `.env` are **never committed**
- Use environment variables for all secrets
- Follow data governance policies for sensitive health data

---

## 📞 Support & Contact

For questions or issues:
1. Check documentation in `docs/`
2. Review existing problem statements in `docs/objectives/problem_statements/`
3. Contact project team leads

---

## 📄 License

[Add appropriate license information]

---

**Last Updated**: 2026-03-11  
**Project Version**: 1.0.0  
**Python Version**: 3.9+  
**Databricks Runtime**: 13.3.x

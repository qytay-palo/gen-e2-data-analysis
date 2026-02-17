---
description: Gen-E2 Data Analysis Project Initialization
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Development
Rule Name: start-gen-e2-data-analysis-project
Rule Version: latest
-->

Your prompt instructions start here:

We will be starting a new Gen-e2 Project

Ask the following questions before proceeding:
## Questions to Ask
1. **Project Objectives**: 
   - What specific business decision will this analysis drive? What happens if we don't do this?
   - Success Metrics: How will we measure if this project succeeded? What does "good enough" look like?

2. **Technical Environment** (review: tech-stack.md)
   - Target platform: HEALIX/Databricks or MCDR/CDSW?
   - Expected data volume and processing needs?

3. **Problem Discovery**:
   - Who are the key stakeholders, and what are their expectations?
   - Who will participate in problem identification workshops?
   - What pain points or questions have stakeholders raised?

## Actions Based on Answers

1. **Update Project Folder Structure**:
Below is the base folder structure:
```
.
├── .env.example      # [PHASE 0] Template for environment variables (DB credentials, API keys)
├── .gitignore        # [PHASE 0] Files to exclude from version control
├── README.md         # [PHASE 0] Project overview and setup instructions
├── requirements.txt  # [PHASE 0] Python dependencies
├── environment.yml   # [PHASE 0] Conda environment (optional)
├── .github/          # [PHASE 0] GitHub Actions & CI/CD
│   └── workflows/
│       ├── data_quality_checks.yml  # → Automated data validation
│       └── scheduled_extraction.yml # → Scheduled ETL jobs
├── docs/             # [PHASE 1] Context & Understanding
│   ├── index.md         # → 1: Central documentation hub (navigation)
│   ├── objectives/      # → 2: PROJECT GOALS: What to achieve
│   ├── data_dictionary/ # → 3: Understand data: schemas, fields, definitions
│   └── methodology/     # → 4: Understand approach: statistical methods, frameworks
├── config/           # [PHASE 2] Project Configuration
│   └── *.yml, *.json       # → Parameters, settings, environment configs
├── sql/              # [PHASE 2] SQL Queries & Database Scripts
│   ├── views/         # → SQL views for common queries
│   ├── procedures/    # → Stored procedures
│   └── extractions/   # → Data extraction queries
├── data/             # [PHASE 3] Data Acquisition & Preparation
│   ├── 1_raw/         # → 1: Original immutable source data
│   ├── 2_external/    # → 2: External reference data (demographics, benchmarks)
│   ├── 3_interim/     # → 3: Intermediate transformation outputs
│   ├── 4_processed/   # → 4: Final cleaned datasets (analysis-ready)
│   └── schemas/       # → Data schemas, contracts, and lineage documentation
├── notebooks/        # [PHASE 4] Interactive Exploration & Analysis
│   ├── 1_exploratory/   # → 1: Initial EDA, data profiling, hypothesis generation
│   └── 2_analysis/      # → 2: Deep-dive analysis, final insights, documentation
│   └── 3_feature_engineering/ # → 3: Feature creation, variable transformations 
├── src/              # [PHASE 5] Production Code Development
│   ├── utils/           # → Foundation: Helper functions, common utilities
│   ├── data_processing/ # → Pipeline 1: ETL, cleaning, validation
│   ├── features/        # → Pipeline 2: Feature engineering, variable transformations
│   ├── analysis/        # → Pipeline 3: Statistical analysis, algorithms
│   ├── visualization/   # → Pipeline 4: Chart generation, plotting utilities
│   └── models/          # → Pipeline 5: Model training, hyperparameter tuning
├── tests/            # [PHASE 6] Quality Assurance
│   ├── unit/          # → Unit tests for individual functions
│   ├── integration/   # → Integration tests for pipelines
│   └── data/          # → Data validation tests
├── models/           # [PHASE 7] Model Development & Storage
│   └── *.pkl, *.h5, *.joblib # → Trained models, model artifacts, serialized objects
├── results/          # [PHASE 8] Analysis Outputs
│   ├── tables/        # → Output 1: Summary statistics, analytical tables (CSV/Excel)
│   ├── metrics/       # → Output 2: Performance KPIs, evaluation metrics (JSON/CSV)
│   └── exports/       # → Output 3: Stakeholder-ready data exports
├── reports/          # [PHASE 9] Stakeholder Communication
│   ├── figures/       # → Component 1: Static visualizations (PNG/PDF)
│   ├── dashboards/    # → Component 2: Interactive dashboards (HTML/Streamlit)
│   └── presentations/ # → Component 3: Executive summaries (PPTX/PDF)
├── logs/             # [PHASE 10] Execution Logs & Audit Trails
│   ├── etl/           # → ETL pipeline execution logs
│   ├── errors/        # → Error logs and stack traces
│   └── audit/         # → Audit trails for data access and changes
└── scripts/          # [PHASE 10] Automation & Deployment
    └── *.py, *.R, *.sh  # → End-to-end pipelines, deployment scripts, automation
```
   - update the project structure based on the answers
   - Update the README.md file, docs/index.md, and create necessary configuration files in the config/ directory to reflect the technical environment and project specifics.

2. **Technical Stack Reference**
   - **Preferred Technologies**: 
      - Consult `docs/project_context/tech-stack.md` for approved platforms and tools

   - **Technology Selection Criteria**:
      1. **Default**: Use technologies from the approved tech stack when they meet project requirements
      2. **Exception**: Propose alternatives only when the approved stack has clear limitations for specific use cases (e.g., specialized libraries, performance and cost constraints, integration requirements)
      3. **Justification Required**: When suggesting alternatives, explicitly state why the approved stack is insufficient and how the alternative addresses the gap
      4. **User Approval**: Obtain explicit approval from project stakeholders before adopting any non-preferred technologies

   - **Actions**:
      - Update project dependencies, environment setup, and documentation based on selected technologies
      - Ensure compatibility with target deployment environment (HEALIX/GCC or MCDR/on-premise)
      - set up appropriate configuration files for the chosen technologies
      - document the chosen platform in README.md and docs/index.md
      - include language specific dependencies in requirements.txt or environment.yml
      - **Mandatory**: Use Polars for data processing and manipulation (preferred over pandas for performance and memory efficiency)
         - Include `polars` in requirements.txt
         - Document Polars usage patterns in project documentation
         - Use Polars for ETL pipelines, data transformations, and feature engineering

3. **Data Dictionary Creation**:
   - Compile a comprehensive data dictionary in `docs/data_dictionary/` that details all datasets, including:
     - Field definitions, data types, and value ranges
     - Data quality notes and known limitations
     - Lineage tracking (source system → transformations → final table)
     - Business owners or subject matter experts for each data domain
     - Refresh frequency and update schedules
     - Sample data and example values
   - Create a master index file that links to individual data dictionary files for each major data domain
   - Ensure the data dictionary is easily navigable and linked from the main documentation index (docs/index.md)

4. **Data Connection Scripts**:
   - refer to `stages/data_extraction.prompt.md` for detailed requirements on data extraction and connection scripts.
   - Create connection scripts in `src/data_processing/` for external data sources (e.g., Kaggle, AWS S3, Azure Blob Storage, APIs). Each script should include authentication handling, connection setup, error handling, and logging. Use environment variables from `.env` for credentials and API keys. Include retry logic for network failures and implement rate limiting for API calls. Document connection parameters and authentication methods in comments. Add connection testing functions to validate credentials before data extraction. Consider creating a base connection class that other connectors can inherit from for consistency.

5. **Code Quality**:
   - Suggest tools for code quality checks, such as linters and formatters.

6. **Create TODO.md**:
   - Create the `TODO.md` file and split it in a way that makes sense for this project.
   - Format:
     ```
     ## Domain
     [ ] Task to be done (owner)
     ```
   - Add tasks for each area of the project, like front-end, back-end, infra, etc.
   - Ensure tasks are detailed and small enough to be done in a few hours.
   - Include tasks outside of development, like DevOps tasks, security tasks, etc.
   - Add lines regarding reviewing all generated files (like Architecture or API doc) and updating them as needed.

7. **Documentation**:
   - If the project is API-First or has an API, suggest a swagger file `docs/apidoc.yaml` .

8. **Tools and Dependencies**:
   - Suggest tools that could be useful for this project, like a specific database, etc.
   - Create all necessary files for the project, like the .gitignore, the .gitattributes, etc.
   - Depending on the selected language, create the necessary files for it (like a requirements.txt for python).
   - If a virtual environment is needed, suggest it and create it. Load all dependencies needed for the project.

9. **Version Control**:
   - Ensure to initialize a Git repository and create an initial commit.

10. **Testing**:
   - Set up testing frameworks and write initial test cases.

11. **Environment Configuration**:
   - Provide guidelines for handling environment variables and secrets (e.g., using .env files).

12. **Code Quality**:
   - Suggest tools for code quality checks, such as linters and formatters.

---

## Final Steps
1. **Update Project Structure**:
   - Reorganize folders following the numbered workflow sequence above
   - Update README.md with project overview, workflow guidance, and technical stack specifications
   - Update docs/index.md to reflect the new structure and technical environment
   - Create environment-specific configuration files based on identified tools and platforms

2. **Install Project Dependencies**:
   - Install all necessary packages and libraries as per the chosen technical stack
   -
   - Document installation steps in README.md and requirements.txt/environment.yml

3. **Review**:
   - Once all the other files are created, and you're clear on the requirements, review the gitignore files, as you might want to add more (like venv or node_modules).

4. **Check File Creation**:
   - Ensure that all the necessary files and folders have been created as per the project structure.

5. **Deploy Requirements**:
   - Run the necessary commands to deploy all the dependencies listed in the requirements files (e.g., `npm install` for Node.js, `pip install -r requirements.txt` for Python).
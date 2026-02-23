# Gen-E2 Data Analysis Project

## Project Overview
This project analyzes temporal patterns across infectious diseases in Singapore to identify seasonal trends and forecast outbreak periods. It also prioritizes resource allocation based on disease burden.

### Key Objectives
- Identify diseases with strong seasonality (Dengue, HFMD, influenza-like illnesses)
- Forecast high-risk periods for proactive resource allocation
- Determine top contributors to infectious disease burden
- Guide public health resource allocation

### Success Criteria
- Comprehensive answers to all above questions

## Technical Environment
- Platform: HEALIX / Databricks
- Data volume: 434 KB
- Stakeholders: Minister of Health, internal committee members

## Workflow
1. Context & Documentation
2. Configuration
3. Data Acquisition & Preparation
4. Interactive Analysis
5. Production Code
6. Testing & QA
7. Model Development
8. Results & Outputs
9. Stakeholder Communication
10. Logging & Audit
11. Automation & Deployment

## Tech Stack
- Python 3.9+
- Polars (mandatory for data processing)
- Databricks integration

## Setup
1. Create virtual environment: `python3 -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `uv pip install -r requirements.txt`

## Folder Structure
See docs/index.md for detailed structure.

## Environment Variables
- See .env.example for template

## Testing
- Run tests with `pytest`

## Code Quality
- Use loguru for logging
- Use linters and formatters (ruff, black)

## Data Dictionary
- See docs/data_dictionary/

## Contact
- Project stakeholders: Minister of Health, internal committee

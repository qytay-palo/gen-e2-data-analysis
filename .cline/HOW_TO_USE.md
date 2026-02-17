# How to Use Claude Data Plugins with Cline

## Available MCP Servers for Data Analysis

I've configured these MCP servers for your MOH data analysis project:

### 1. **Filesystem Server** ✓ Enabled
**What it does**: Direct file system access for data files
**Tools available**:
- `read_file` - Read data files
- `write_file` - Write processed data
- `list_directory` - Browse data folders
- `create_directory` - Organize outputs
- `move_file` - Reorganize files

**Use cases**:
```
"Read the CSV file in data/1_raw/hospital_visits.csv and analyze it"
"List all files in data/3_interim/"
"Create a new directory for today's analysis results"
```

### 2. **SQLite Server** ✓ Enabled
**What it does**: Query and analyze SQLite databases
**Tools available**:
- Execute SQL queries
- Create/update tables
- Data aggregation and joins

**Use cases**:
```
"Query the patient_records database for admission trends"
"Create a summary table of emergency visits by month"
"Join the diagnosis and treatment tables"
```

### 3. **GitHub Server** ⚠️ Disabled (needs token)
**What it does**: Search code, create issues, manage repos
**To enable**: Add your GitHub token to the config

## How to Use with Cline

### Step 1: Open Cline
1. Click the Cline icon in your VS Code sidebar
2. Or press `Cmd+Shift+P` → "Cline: Focus on Chat View"

### Step 2: Start a Conversation
Cline will automatically have access to the MCP tools. Just chat naturally:

**Example conversations:**

#### Data Exploration
```
You: "Using the filesystem tools, list all CSV files in data/1_raw/ 
and show me the first 5 rows of each"

Cline: [Uses read_file and list_directory tools automatically]
```

#### Data Analysis
```
You: "Read data/1_raw/emergency_visits.csv and:
1. Calculate monthly visit trends
2. Identify peak hours
3. Create visualizations in reports/figures/"

Cline: [Reads file, performs analysis, saves outputs]
```

#### Database Queries
```
You: "Query the SQLite database to find:
- Total hospital admissions by region
- Average wait times by department
- Trends over the last 6 months"

Cline: [Executes SQL queries via SQLite MCP server]
```

### Step 3: Using Your Prompt Files

You can reference your prompt files in `.github/prompts/`:

```
You: "Follow the workflow in .github/prompts/stages/data_extraction.prompt.md
to extract data from the Kaggle dataset"

Cline: [Follows the structured prompt, uses MCP tools as needed]
```

Or:

```
You: "Execute the implementation plan in 
.github/prompts/5-execute-implementation-plan.prompt.md
Use the filesystem MCP tools to create the required files"

Cline: [Executes plan using MCP tools for file operations]
```

## Real-World Data Analysis Workflow

### Complete Example: Hospital Visit Analysis

```
You: "I need to analyze emergency department visits. Here's the workflow:

1. List all CSV files in data/1_raw/
2. Read the emergency_visits.csv file
3. Perform exploratory data analysis:
   - Check for missing values
   - Calculate summary statistics
   - Identify outliers
4. Create visualizations:
   - Time series of visits by hour
   - Heat map of visits by day/hour
   - Distribution of wait times
5. Save outputs to:
   - Cleaned data: data/4_processed/emergency_visits_clean.csv
   - Figures: reports/figures/emergency_analysis/
   - Summary: reports/emergency_visits_summary.md

Use the MCP filesystem tools to handle all file operations."

Cline: [Executes entire workflow using MCP tools]
```

## MCP Tools vs Regular Cline

**Without MCP tools**:
- Cline asks you to paste file contents
- Manual file creation/editing
- Limited database access

**With MCP tools**:
- ✓ Direct file system access
- ✓ Automatic file reading/writing
- ✓ Database queries
- ✓ Organized file operations
- ✓ Faster, more autonomous workflow

## Best Practices

### 1. Be Specific About Data Locations
```
Good: "Read data/1_raw/hospital_visits.csv"
Bad: "Read the hospital data"
```

### 2. Request Multiple Operations
```
"Using filesystem tools:
1. Create directory reports/2026-02-06/
2. Read all CSVs in data/1_raw/
3. Save analysis to the new directory"
```

### 3. Leverage Your Project Structure
```
"Following the project structure:
- Read from data/1_raw/
- Process and save to data/3_interim/
- Generate reports in reports/figures/"
```

### 4. Combine with Your Prompts
```
"Use the stage prompt in .github/prompts/stages/analyse.prompt.md
and the filesystem MCP tools to complete the analysis"
```

## Verifying MCP Connection

To check if MCP servers are working:

1. **Open Cline settings** (gear icon in Cline panel)
2. **Look for "MCP Servers"** section
3. **You should see**:
   - ✓ filesystem (Connected)
   - ✓ sqlite (Connected)
   - ⚠️ github (Disabled - needs token)

4. **Test with a simple command**:
```
You: "Use the filesystem tools to list the contents of data/1_raw/"

Cline: [Should show directory listing using MCP tool]
```

## Adding More MCP Servers

Browse available servers at: https://github.com/modelcontextprotocol/servers

Popular ones for data analysis:
- **PostgreSQL** - For PostgreSQL databases
- **Google Drive** - Access Google Sheets/Docs
- **Slack** - Team notifications
- **Brave Search** - Web research for context

To add, edit `.cline/mcp_settings.json` and follow the same pattern.

## Troubleshooting

### MCP servers not showing up
1. Restart VS Code
2. Check Cline output panel for errors
3. Ensure Node.js is installed: `node --version`

### "Permission denied" errors
Add the tool to `alwaysAllow` in mcp_settings.json

### SQLite server not connecting
Ensure the database path exists in your data/ directory

## Integration with Your MOH Project

For your MOH data analysis project, use Cline with MCP tools to:

1. **Data Extraction** (Epic 001-004)
   - Read raw Kaggle data
   - Extract specific datasets
   - Organize by epic/user story

2. **Data Quality Checks**
   - Validate data completeness
   - Check data types
   - Generate quality reports

3. **Exploratory Analysis**
   - Calculate statistics
   - Generate visualizations
   - Document findings

4. **Feature Engineering**
   - Create derived features
   - Save processed datasets
   - Track transformations

All automated through Cline + MCP tools!

## Quick Reference Card

| Task | Command Example |
|------|-----------------|
| **List data files** | "List all CSV files in data/1_raw/" |
| **Read data** | "Read and summarize data/1_raw/visits.csv" |
| **Create directory** | "Create directory results/2026-02-06/" |
| **Query database** | "Query SQLite for patient admission trends" |
| **Save analysis** | "Save this analysis to reports/analysis.md" |
| **Follow prompt** | "Execute .github/prompts/stages/eda.prompt.md" |
| **Complete workflow** | "Follow the workflow in prompt X using filesystem tools" |

---

**Next**: Open Cline and try: 
```
"List the contents of data/1_raw/ using the filesystem MCP tools"
```

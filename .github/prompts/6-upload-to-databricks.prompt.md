# Databricks Upload Guide for Data Analysis Projects

**Role**: You are a **Data Engineer / MLOps Specialist** with expertise in Python and Databricks. Your responsibility is to migrate the complete end to end data analysis project from local development to Databricks production environment. This includes uploading raw/processed data, notebooks, Python modules, configuration files, and dashboards while maintaining proper data governance through Unity Catalog.

This guide provides comprehensive instructions for uploading local data analysis artifacts to Databricks workspace using multiple approaches.

---

## Prerequisites & Installation

### 1. Install Required Packages

```bash
# Using uv (preferred for this project)
uv pip install databricks-cli databricks-sdk databricks-connect --upgrade
```

---

## Initial Setup (For First-Time Users)

⚠️ **IMPORTANT**: Complete these steps BEFORE running any upload scripts.

### Step 1: Access Your Databricks Workspace

**What you need:**
- Your Databricks workspace URL (e.g., `https://your-company.cloud.databricks.com`)
- Login credentials to your Databricks account

**Action:**
1. Open your web browser and navigate to your Databricks workspace URL
2. Log in with your credentials
3. Keep this window open for the next step

---

### Step 2: Generate Personal Access Token (PAT)

**Why:** The token authenticates your local machine to upload files securely to Databricks.

**Instructions:**
1. In Databricks workspace, click your username (top-right corner)
2. Select **Settings** → **Developer** → **Access tokens**
3. Click **Generate new token**
4. Configure token settings:
   - **Comment**: "Local data analysis uploads" (or descriptive name)
   - **Lifetime**: 90 days (or as per your organization's policy)
   - **Scopes** (select these permissions):
     - ✅ `access-management` - Manage workspace access
     - ✅ `apps` - Upload applications/dashboards
     - ✅ `dashboards` - Create/update dashboards
     - ✅ `environments` - Configure runtime environments
     - ✅ `files` - Upload files and data
     - ✅ `libraries` - Install Python packages
     - ✅ `workspace` - Create notebooks and folders
     - ✅ `unity-catalog` - Manage data volumes and catalogs
5. Click **Generate**
6. **⚠️ CRITICAL**: Copy the token immediately and save it securely (it won't be shown again)

**Documentation:** https://docs.databricks.com/en/dev-tools/auth/pat.html

---

### Step 3: Create Configuration File

**What:** A `.databrickscfg` file stores your connection settings for authentication.

**Location:**
- **macOS/Linux**: `~/.databrickscfg` (in your home directory)
- **Windows**: `C:\Users\<YourUsername>\.databrickscfg`

**Instructions:**

1. Create the file using your text editor or terminal:

```bash
# macOS/Linux
nano ~/.databrickscfg

# Windows PowerShell
notepad $env:USERPROFILE\.databrickscfg
```

2. Add the following content (replace placeholders with YOUR values):

```ini
[DEFAULT]
host = https://prod-workspace.cloud.databricks.com
token = default_token_here

# Optional: Add additional profiles for different workspaces
[PRODUCTION]
host = https://prod-workspace.cloud.databricks.com
token = prod_token_here

[DEVELOPMENT]
host = https://dev-workspace.cloud.databricks.com
token = dev_token_here
```

3. Save and close the file
4. Set proper permissions (macOS/Linux only):

```bash
chmod 600 ~/.databrickscfg
```

**Documentation:** https://docs.databricks.com/en/dev-tools/auth/config-profiles.html

---

### Step 4: Verify Connection

Run this test script to verify your setup is correct:

```python
from databricks.sdk import WorkspaceClient

try:
    # Initialize workspace client (reads from ~/.databrickscfg)
    workspace = WorkspaceClient()
    
    # Get current user information
    current_user = workspace.current_user.me()
    
    print("✅ Connection successful!")
    print(f"Logged in as: {current_user.user_name}")
    print(f"User ID: {current_user.id}")
    
except Exception as e:
    print("❌ Connection failed!")
    print(f"Error: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Verify ~/.databrickscfg exists and contains correct host/token")
    print("2. Check token hasn't expired (regenerate if needed)")
    print("3. Ensure workspace URL is correct (include https://)")
    print("4. Confirm network connectivity to Databricks workspace")
```

**Expected Output:**
```
✅ Connection successful!
Logged in as: your.email@company.com
User ID: 1234567890123456
```

---

## Alternative Upload Approaches

### Comparison Matrix

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **Python SDK (Recommended)** | Programmatic uploads, automation | Full control, error handling, batch processing | Requires Python scripting |
| **Databricks CLI** | Quick manual uploads, CI/CD | Simple commands, scriptable | Limited batch operations |
| **Databricks Repos** | Version-controlled code | Git integration, team collaboration | Not for data files >100MB |
| **Workspace UI** | Small files, one-time uploads | No setup needed | Not scalable, manual process |

---

### Approach 1: Python SDK (Recommended for This Project)

**When to use:**
- Uploading multiple files programmatically
- Automating uploads in workflows
- Need fine-grained control and error handling
- Uploading data analysis artifacts (notebooks, data, scripts, configs)

**See detailed implementation in sections below.**

---

### Approach 2: Databricks CLI

**Installation:**
```bash
# macOS (using Homebrew)
brew install databricks/tap/databricks

# Linux/Windows
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Verify installation
databricks --version
```

**Configuration:**
```bash
# Authenticate (interactive)
databricks configure --token

# Or use existing .databrickscfg
databricks auth env --profile DEFAULT
```

**Common Upload Commands:**

```bash
# Upload single notebook
databricks workspace import ./notebook.ipynb /Users/me/notebook --format JUPYTER

# Upload directory recursively
databricks workspace import-dir ./notebooks /Users/me/notebooks --overwrite

# Upload file to DBFS
databricks fs cp ./data.csv dbfs:/FileStore/data.csv --overwrite

# Upload to Unity Catalog volume
databricks fs cp ./data.csv dbfs:/Volumes/catalog/schema/volume/data.csv

# Batch upload data files
databricks fs cp -r ./data/4_processed dbfs:/Volumes/workspace/default/moh_data/processed/
```

**Documentation:** https://docs.databricks.com/en/dev-tools/cli/install.html

---

### Approach 3: Databricks Repos (Git Integration)

**When to use:**
- Version-controlled Python scripts, notebooks, configs
- Team collaboration with code review
- NOT suitable for large data files (>100MB)

**Setup:**

1. Initialize Git repository in your project (if not already):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Push to remote (GitHub, GitLab, Bitbucket, Azure DevOps)

3. In Databricks workspace:
   - Click **Repos** in sidebar
   - Click **Add Repo**
   - Select Git provider and enter repository URL
   - Clone repository

**Pros:**
- Automatic sync with version control
- Built-in code review workflows
- Change tracking and rollback

**Cons:**
- Only for code/notebooks (not data files)
- Requires Git knowledge
- Data files must be uploaded separately

**Recommendation:** Use Repos for `src/` and `notebooks/`, but upload data via SDK/CLI.

---

### Approach 4: Workspace UI (Manual Upload)

**When to use:**
- Quick testing
- Single file uploads
- Small files (<100MB)

**Steps:**
1. Navigate to Databricks workspace
2. Click **Workspace** → navigate to target folder
3. Click **⋮** → **Import** → Select file
4. Choose format (Jupyter, Python, etc.)

**Not recommended** for this project due to multiple files and automation needs. 


---

## Python SDK Implementation (Detailed)

### Initialize Workspace Connection

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat
from databricks.sdk.service.catalog import VolumeType
import base64
import os
from pathlib import Path
from typing import List, Dict, Optional
import json

# Initialize workspace client (reads from ~/.databrickscfg)
workspace = WorkspaceClient()

# Get current user for dynamic paths
current_user = workspace.current_user.me()
USER_NAME = current_user.user_name
print(f"✅ Connected as: {USER_NAME}")

# Define remote workspace structure
WORKSPACE_BASE = f"/Users/{USER_NAME}/moh-data-analysis"
```

---

### 1. Upload Notebooks

**Supports:** `.ipynb` (Jupyter), `.py` (Python), `.sql` (SQL), `.scala` (Scala), `.r` (R)

```python
def upload_notebook_to_databricks(
    local_path: str, 
    remote_path: str, 
    format_type: ImportFormat = ImportFormat.AUTO
) -> bool:
    """
    Upload a notebook file to Databricks workspace.
    
    Args:
        local_path: Path to local notebook file
        remote_path: Destination path in Databricks workspace (without extension)
        format_type: Notebook format (AUTO, JUPYTER, PYTHON, SQL, SCALA, R)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate local file exists
        if not os.path.exists(local_path):
            print(f"❌ File not found: {local_path}")
            return False
        
        # Read and encode content
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        # Auto-detect format if not specified
        if format_type == ImportFormat.AUTO:
            ext = Path(local_path).suffix.lower()
            format_map = {
                '.ipynb': ImportFormat.JUPYTER,
                '.py': ImportFormat.SOURCE,
                '.sql': ImportFormat.SQL,
                '.scala': ImportFormat.SOURCE,
                '.r': ImportFormat.SOURCE
            }
            format_type = format_map.get(ext, ImportFormat.AUTO)
        
        # Create parent directory if needed
        parent_dir = str(Path(remote_path).parent)
        try:
            workspace.workspace.mkdirs(parent_dir)
        except:
            pass  # Directory might already exist
        
        # Upload notebook
        workspace.workspace.import_(
            path=remote_path,
            format=format_type,
            content=encoded_content,
            overwrite=True,
            language=None  # Auto-detect from content
        )
        
        print(f"✅ Uploaded notebook: {local_path} → {remote_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to upload {local_path}: {str(e)}")
        return False


def batch_upload_notebooks(notebook_dir: str, remote_base: str) -> Dict[str, bool]:
    """
    Upload all notebooks from a directory to Databricks.
    
    Args:
        notebook_dir: Local directory containing notebooks
        remote_base: Remote directory path in Databricks
    
    Returns:
        dict: Mapping of file paths to upload status (True/False)
    """
    results = {}
    notebook_extensions = {'.ipynb', '.py', '.sql', '.scala', '.r'}
    
    for root, dirs, files in os.walk(notebook_dir):
        for file in files:
            if Path(file).suffix.lower() in notebook_extensions:
                local_path = os.path.join(root, file)
                
                # Compute relative path for remote structure
                rel_path = os.path.relpath(local_path, notebook_dir)
                remote_path = os.path.join(remote_base, rel_path).replace(os.sep, '/')
                
                # Remove extension for Databricks (it adds automatically)
                remote_path = str(Path(remote_path).with_suffix(''))
                
                success = upload_notebook_to_databricks(local_path, remote_path)
                results[local_path] = success
    
    # Print summary
    total = len(results)
    successful = sum(results.values())
    print(f"\n📊 Upload Summary: {successful}/{total} notebooks uploaded successfully")
    
    return results


# Example: Upload all project notebooks
# results = batch_upload_notebooks(
#     notebook_dir="./notebooks",
#     remote_base=f"{WORKSPACE_BASE}/notebooks"
# )
```



---

### 2. Upload Data Files to Unity Catalog Volumes

**Recommended for:** CSV, Parquet, JSON, Excel files in production

**Unity Catalog Benefits:**
- Fine-grained access control
- Data lineage tracking
- Better organization (catalog → schema → volume structure)
- Supports large files (>2GB)

#### a. Create Unity Catalog Volume

```python
def create_or_get_volume(
    catalog_name: str,
    schema_name: str,
    volume_name: str,
    comment: str = "Data storage volume"
) -> Optional[str]:
    """
    Create a Unity Catalog volume or return existing volume path.
    
    Args:
        catalog_name: Catalog name (e.g., 'workspace', 'main')
        schema_name: Schema name (e.g., 'default', 'moh_analytics')
        volume_name: Volume name (e.g., 'data', 'processed_data')
        comment: Description of the volume
    
    Returns:
        str: Volume path if successful, None otherwise
    """
    volume_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}"
    
    try:
        # Try to create the volume
        volume = workspace.volumes.create(
            catalog_name=catalog_name,
            schema_name=schema_name,
            name=volume_name,
            volume_type=VolumeType.MANAGED,
            comment=comment
        )
        print(f"✅ Volume created: {volume_path}")
        return volume_path
        
    except Exception as e:
        error_msg = str(e)
        if "ALREADY_EXISTS" in error_msg or "already exists" in error_msg.lower():
            print(f"✅ Volume already exists: {volume_path}")
            return volume_path
        else:
            print(f"❌ Error creating volume: {error_msg}")
            print(f"   Make sure catalog '{catalog_name}' and schema '{schema_name}' exist")
            return None


# Example: Create volumes for different data stages
# RAW_VOLUME = create_or_get_volume("workspace", "default", "moh_raw_data", "Raw data from MOH")
# PROCESSED_VOLUME = create_or_get_volume("workspace", "default", "moh_processed_data", "Processed datasets")
# RESULTS_VOLUME = create_or_get_volume("workspace", "default", "moh_results", "Analysis results")
```

#### b. Upload Files to Volume

```python
def upload_file_to_volume(
    local_path: str,
    volume_path: str,
    remote_filename: Optional[str] = None,
    show_progress: bool = True
) -> bool:
    """
    Upload a file to Databricks Unity Catalog volume.
    
    Args:
        local_path: Path to local file
        volume_path: Volume path (e.g., '/Volumes/workspace/default/my_volume')
        remote_filename: Optional custom filename (defaults to local filename)
        show_progress: Whether to show upload progress
    
    Returns:
        bool: True if successful
    """
    try:
        # Validate local file
        if not os.path.exists(local_path):
            print(f"❌ File not found: {local_path}")
            return False
        
        # Determine remote filename
        if remote_filename is None:
            remote_filename = os.path.basename(local_path)
        
        remote_path = f"{volume_path}/{remote_filename}"
        
        # Get file size for progress
        file_size = os.path.getsize(local_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if show_progress:
            print(f"📤 Uploading {local_path} ({file_size_mb:.2f} MB)...")
        
        # Upload using Files API (for volumes)
        with open(local_path, 'rb') as f:
            workspace.files.upload(
                file_path=remote_path,
                contents=f,
                overwrite=True
            )
        
        print(f"✅ Uploaded: {local_path} → {remote_path}")
        return True
        
    except Exception as e:
        print(f"❌ Upload failed for {local_path}: {str(e)}")
        return False


def batch_upload_data_files(
    local_dir: str,
    volume_path: str,
    file_patterns: List[str] = ['*.csv', '*.parquet', '*.json', '*.xlsx'],
    preserve_structure: bool = True
) -> Dict[str, bool]:
    """
    Upload multiple data files from a directory to a volume.
    
    Args:
        local_dir: Local directory containing data files
        volume_path: Target volume path
        file_patterns: List of file patterns to match (e.g., ['*.csv', '*.parquet'])
        preserve_structure: Whether to preserve subdirectory structure
    
    Returns:
        dict: Mapping of file paths to upload status
    """
    results = {}
    
    for pattern in file_patterns:
        for local_path in Path(local_dir).rglob(pattern):
            if local_path.is_file():
                # Compute remote path
                if preserve_structure:
                    rel_path = local_path.relative_to(local_dir)
                    remote_file = str(rel_path).replace(os.sep, '/')
                else:
                    remote_file = local_path.name
                
                success = upload_file_to_volume(
                    str(local_path),
                    volume_path,
                    remote_filename=remote_file,
                    show_progress=True
                )
                results[str(local_path)] = success
    
    # Summary
    total = len(results)
    successful = sum(results.values())
    print(f"\n📊 Upload Summary: {successful}/{total} files uploaded successfully")
    
    return results


# Example: Upload all processed data files
# PROCESSED_VOLUME = "/Volumes/workspace/default/moh_processed_data"
# results = batch_upload_data_files(
#     local_dir="./data/4_processed",
#     volume_path=PROCESSED_VOLUME,
#     file_patterns=['*.csv', '*.parquet'],
#     preserve_structure=True
# )
```

---

### 3. Upload Python Scripts and Modules

**For:** `.py` files that are reusable modules (not notebooks)

```python
def upload_python_script(
    local_path: str,
    remote_path: str,
    as_notebook: bool = False
) -> bool:
    """
    Upload a Python script to Databricks workspace.
    
    Args:
        local_path: Path to .py file
        remote_path: Destination path in workspace
        as_notebook: If True, import as executable notebook; if False, as source file
    
    Returns:
        bool: Success status
    """
    try:
        if not os.path.exists(local_path):
            print(f"❌ File not found: {local_path}")
            return False
        
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        # Create parent directory
        parent_dir = str(Path(remote_path).parent)
        try:
            workspace.workspace.mkdirs(parent_dir)
        except:
            pass
        
        # Import as notebook or source
        import_format = ImportFormat.SOURCE if not as_notebook else ImportFormat.PYTHON
        
        workspace.workspace.import_(
            path=remote_path,
            format=import_format,
            content=encoded_content,
            overwrite=True,
            language=None
        )
        
        print(f"✅ Uploaded Python script: {local_path} → {remote_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to upload {local_path}: {str(e)}")
        return False


def batch_upload_src_modules(
    src_dir: str = "./src",
    remote_base: str = None
) -> Dict[str, bool]:
    """
    Upload all Python modules from src/ directory.
    
    Args:
        src_dir: Local src directory
        remote_base: Remote workspace path (defaults to /Users/{user}/moh-data-analysis/src)
    
    Returns:
        dict: Upload results
    """
    if remote_base is None:
        remote_base = f"{WORKSPACE_BASE}/src"
    
    results = {}
    
    for py_file in Path(src_dir).rglob('*.py'):
        if py_file.is_file() and '__pycache__' not in str(py_file):
            local_path = str(py_file)
            rel_path = py_file.relative_to(src_dir)
            remote_path = f"{remote_base}/{rel_path}".replace(os.sep, '/')
            
            success = upload_python_script(local_path, remote_path, as_notebook=False)
            results[local_path] = success
    
    total = len(results)
    successful = sum(results.values())
    print(f"\n📊 Uploaded {successful}/{total} Python modules")
    
    return results


# Example: Upload all source code modules
# results = batch_upload_src_modules(
#     src_dir="./src",
#     remote_base=f"{WORKSPACE_BASE}/src"
# )
```

---

### 4. Upload Configuration Files

```python
def upload_config_files(
    config_dir: str = "./config",
    remote_base: str = None
) -> Dict[str, bool]:
    """
    Upload configuration files (YAML, JSON, TOML) to Databricks.
    
    Args:
        config_dir: Local config directory
        remote_base: Remote workspace path
    
    Returns:
        dict: Upload results
    """
    if remote_base is None:
        remote_base = f"{WORKSPACE_BASE}/config"
    
    results = {}
    config_extensions = {'.yml', '.yaml', '.json', '.toml', '.ini'}
    
    for config_file in Path(config_dir).rglob('*'):
        if config_file.is_file() and config_file.suffix in config_extensions:
            local_path = str(config_file)
            rel_path = config_file.relative_to(config_dir)
            remote_path = f"{remote_base}/{rel_path}".replace(os.sep, '/')
            
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                # Create parent directory
                parent_dir = str(Path(remote_path).parent)
                try:
                    workspace.workspace.mkdirs(parent_dir)
                except:
                    pass
                
                workspace.workspace.import_(
                    path=remote_path,
                    format=ImportFormat.AUTO,
                    content=encoded,
                    overwrite=True
                )
                
                print(f"✅ Uploaded config: {local_path} → {remote_path}")
                results[local_path] = True
                
            except Exception as e:
                print(f"❌ Failed to upload {local_path}: {str(e)}")
                results[local_path] = False
    
    return results


# Example: Upload all config files
# config_results = upload_config_files(
#     config_dir="./config",
#     remote_base=f"{WORKSPACE_BASE}/config"
# )
```

---

### 5. Upload Dashboard Files

```python
def upload_dashboard_app(
    dashboard_dir: str = "./dashboards",
    remote_base: str = None
) -> Dict[str, bool]:
    """
    Upload Streamlit dashboard files to Databricks.
    
    Args:
        dashboard_dir: Local dashboard directory
        remote_base: Remote workspace path
    
    Returns:
        dict: Upload results
    """
    if remote_base is None:
        remote_base = f"{WORKSPACE_BASE}/dashboards"
    
    results = {}
    dashboard_extensions = {'.py', '.md'}
    
    for item in Path(dashboard_dir).rglob('*'):
        if item.is_file() and (item.suffix in dashboard_extensions or item.name.endswith('requirements.txt')):
            if '__pycache__' in str(item):
                continue
                
            local_path = str(item)
            rel_path = item.relative_to(dashboard_dir)
            remote_path = f"{remote_base}/{rel_path}".replace(os.sep, '/')
            
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                # Create parent directory
                parent_dir = str(Path(remote_path).parent)
                try:
                    workspace.workspace.mkdirs(parent_dir)
                except:
                    pass
                
                # Determine format
                if item.suffix == '.py':
                    format_type = ImportFormat.SOURCE
                else:
                    format_type = ImportFormat.AUTO
                
                workspace.workspace.import_(
                    path=remote_path,
                    format=format_type,
                    content=encoded,
                    overwrite=True
                )
                
                print(f"✅ Uploaded dashboard file: {local_path} → {remote_path}")
                results[local_path] = True
                
            except Exception as e:
                print(f"❌ Failed to upload {local_path}: {str(e)}")
                results[local_path] = False
    
    return results
    
# Example: Upload dashboards
# dashboard_results = upload_dashboard_app(
#     dashboard_dir="./dashboards",
#     remote_base=f"{WORKSPACE_BASE}/dashboards"
# )
```
---

## End-to-End Upload Orchestration

### Complete Project Upload Script

This script uploads all data analysis artifacts in the correct order.

```python
import time
from datetime import datetime

def upload_complete_project(
    catalog_name: str = "workspace",
    schema_name: str = "default",
    project_name: str = "moh_data_analysis"
) -> Dict[str, any]:
    """
    Upload entire data analysis project to Databricks.
    
    Args:
        catalog_name: Unity Catalog name
        schema_name: Schema name
        project_name: Project identifier
    
    Returns:
        dict: Summary of upload results
    """
    print("=" * 70)
    print("🚀 DATABRICKS PROJECT UPLOAD - MOH Data Analysis")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    upload_summary = {
        'timestamp': datetime.now().isoformat(),
        'catalog': catalog_name,
        'schema': schema_name,
        'project': project_name,
        'results': {}
    }
    
    # Step 1: Create Unity Catalog volumes
    print("\n" + "=" * 70)
    print("STEP 1: Creating Unity Catalog Volumes")
    print("=" * 70)
    
    volumes = {
        'raw_data': create_or_get_volume(catalog_name, schema_name, f"{project_name}_raw_data", "Raw datasets from MOH"),
        'processed_data': create_or_get_volume(catalog_name, schema_name, f"{project_name}_processed_data", "Cleaned and processed datasets"),
        'results': create_or_get_volume(catalog_name, schema_name, f"{project_name}_results", "Analysis results and metrics"),
    }
    upload_summary['volumes'] = volumes
    print(f"✅ Created {len([v for v in volumes.values() if v])} volumes")
    
    # Step 2: Upload raw data files
    print("\n" + "=" * 70)
    print("STEP 2: Uploading Raw Data Files")
    print("=" * 70)
    
    if volumes['raw_data'] and os.path.exists('./data/1_raw'):
        raw_results = batch_upload_data_files(
            local_dir='./data/1_raw',
            volume_path=volumes['raw_data'],
            file_patterns=['*.csv', '*.xlsx', '*.json'],
            preserve_structure=True
        )
        upload_summary['results']['raw_data'] = raw_results
    else:
        print("⚠️  Skipping: Raw data directory not found or volume creation failed")
        upload_summary['results']['raw_data'] = {}
    
    # Step 3: Upload processed data files
    print("\n" + "=" * 70)
    print("STEP 3: Uploading Processed Data Files")
    print("=" * 70)
    
    if volumes['processed_data'] and os.path.exists('./data/4_processed'):
        processed_results = batch_upload_data_files(
            local_dir='./data/4_processed',
            volume_path=volumes['processed_data'],
            file_patterns=['*.csv', '*.parquet', '*.json'],
            preserve_structure=True
        )
        upload_summary['results']['processed_data'] = processed_results
    else:
        print("⚠️  Skipping: Processed data directory not found or volume creation failed")
        upload_summary['results']['processed_data'] = {}
    
    # Step 4: Upload results and metrics
    print("\n" + "=" * 70)
    print("STEP 4: Uploading Analysis Results")
    print("=" * 70)
    
    if volumes['results'] and os.path.exists('./results'):
        results_upload = batch_upload_data_files(
            local_dir='./results',
            volume_path=volumes['results'],
            file_patterns=['*.csv', '*.json', '*.parquet'],
            preserve_structure=True
        )
        upload_summary['results']['results'] = results_upload
    else:
        print("⚠️  Skipping: Results directory not found or volume creation failed")
        upload_summary['results']['results'] = {}
    
    # Step 5: Upload notebooks
    print("\n" + "=" * 70)
    print("STEP 5: Uploading Jupyter Notebooks")
    print("=" * 70)
    
    if os.path.exists('./notebooks'):
        notebook_results = batch_upload_notebooks(
            notebook_dir='./notebooks',
            remote_base=f"{WORKSPACE_BASE}/notebooks"
        )
        upload_summary['results']['notebooks'] = notebook_results
    else:
        print("⚠️  Skipping: Notebooks directory not found")
        upload_summary['results']['notebooks'] = {}
    
    # Step 6: Upload Python source modules
    print("\n" + "=" * 70)
    print("STEP 6: Uploading Python Source Code")
    print("=" * 70)
    
    if os.path.exists('./src'):
        src_results = batch_upload_src_modules(
            src_dir='./src',
            remote_base=f"{WORKSPACE_BASE}/src"
        )
        upload_summary['results']['src'] = src_results
    else:
        print("⚠️  Skipping: Source directory not found")
        upload_summary['results']['src'] = {}
    
    # Step 7: Upload configuration files
    print("\n" + "=" * 70)
    print("STEP 7: Uploading Configuration Files")
    print("=" * 70)
    
    if os.path.exists('./config'):
        config_results = upload_config_files(
            config_dir='./config',
            remote_base=f"{WORKSPACE_BASE}/config"
        )
        upload_summary['results']['config'] = config_results
    else:
        print("⚠️  Skipping: Config directory not found")
        upload_summary['results']['config'] = {}
    
    # Step 8: Upload dashboards
    print("\n" + "=" * 70)
    print("STEP 8: Uploading Dashboards")
    print("=" * 70)
    
    if os.path.exists('./dashboards'):
        dashboard_results = upload_dashboard_app(
            dashboard_dir='./dashboards',
            remote_base=f"{WORKSPACE_BASE}/dashboards"
        )
        upload_summary['results']['dashboards'] = dashboard_results
    else:
        print("⚠️  Skipping: Dashboards directory not found")
        upload_summary['results']['dashboards'] = {}
    
    # Print final summary
    print("\n" + "=" * 70)
    print("📊 UPLOAD SUMMARY")
    print("=" * 70)
    
    total_files = 0
    successful_files = 0
    
    for category, results in upload_summary['results'].items():
        if isinstance(results, dict):
            cat_total = len(results)
            cat_success = sum(results.values())
            total_files += cat_total
            successful_files += cat_success
            
            status = "✅" if cat_success == cat_total else "⚠️"
            print(f"{status} {category.upper()}: {cat_success}/{cat_total} files")
    
    print(f"\n{'=' * 70}")
    print(f"🎯 TOTAL: {successful_files}/{total_files} files uploaded successfully")
    print(f"⏱️  Duration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 70}\n")
    
    # Save upload log
    log_file = f"./logs/databricks_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('./logs', exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(upload_summary, f, indent=2)
    print(f"📝 Upload log saved to: {log_file}\n")
    
    return upload_summary


# Execute complete upload
# upload_summary = upload_complete_project(
#     catalog_name="workspace",
#     schema_name="default",
#     project_name="moh_data_analysis"
# )
```

---

## Verification & Validation

### Verify Upload Success

```python
def verify_workspace_structure(base_path: str = None) -> bool:
    """
    Verify that project files were uploaded correctly to Databricks workspace.
    
    Args:
        base_path: Workspace base path (defaults to WORKSPACE_BASE)
    
    Returns:
        bool: True if structure is valid
    """
    if base_path is None:
        base_path = WORKSPACE_BASE
    
    print(f"🔍 Verifying workspace structure at: {base_path}\n")
    
    expected_dirs = [
        f"{base_path}/notebooks",
        f"{base_path}/src",
        f"{base_path}/config",
        f"{base_path}/dashboards"
    ]
    
    all_exist = True
    
    for dir_path in expected_dirs:
        try:
            items = workspace.workspace.list(dir_path)
            item_count = len(list(items))
            print(f"✅ {dir_path} ({item_count} items)")
        except Exception as e:
            print(f"❌ {dir_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def verify_volumes(
    catalog_name: str = "workspace",
    schema_name: str = "default",
    volume_prefix: str = "moh_data_analysis"
) -> bool:
    """
    Verify that Unity Catalog volumes exist and contain files.
    
    Args:
        catalog_name: Catalog name
        schema_name: Schema name
        volume_prefix: Volume name prefix
    
    Returns:
        bool: True if volumes are valid
    """
    print(f"🔍 Verifying volumes in {catalog_name}.{schema_name}\n")
    
    volume_names = [f"{volume_prefix}_raw_data", f"{volume_prefix}_processed_data", f"{volume_prefix}_results"]
    
    all_exist = True
    
    for volume_name in volume_names:
        try:
            volume_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}"
            files = workspace.files.list_directory_contents(volume_path)
            file_count = len(list(files))
            print(f"✅ {volume_name} ({file_count} files)")
        except Exception as e:
            print(f"❌ {volume_name} - NOT FOUND or EMPTY")
            all_exist = False
    
    return all_exist


# Run verification
# workspace_valid = verify_workspace_structure()
# volumes_valid = verify_volumes()
# 
# if workspace_valid and volumes_valid:
#     print("\n✅ All verifications passed!")
# else:
#     print("\n⚠️  Some verifications failed. Review output above.")
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Errors

**Error:** `DatabricksError: Authentication required`

**Solutions:**
```python
# Check if config file exists
import os
config_path = os.path.expanduser("~/.databrickscfg")
print(f"Config exists: {os.path.exists(config_path)}")

# Read config file
with open(config_path, 'r') as f:
    print(f.read())

# Verify token hasn't expired (regenerate if needed)
# Ensure host URL is correct (include https://)
```

---

#### 2. Volume Creation Fails

**Error:** `SCHEMA_NOT_FOUND` or `CATALOG_NOT_FOUND`

**Solutions:**
```python
# List available catalogs
try:
    catalogs = workspace.catalogs.list()
    print("Available catalogs:")
    for cat in catalogs:
        print(f"  - {cat.name}")
except Exception as e:
    print(f"Error listing catalogs: {e}")

# List schemas in a catalog
try:
    schemas = workspace.schemas.list(catalog_name="workspace")
    print("Available schemas:")
    for schema in schemas:
        print(f"  - {schema.name}")
except Exception as e:
    print(f"Error listing schemas: {e}")

# Create schema if needed
# workspace.schemas.create(catalog_name="workspace", name="moh_analytics")
```

---

#### 3. File Upload Fails

**Error:** `RESOURCE_DOES_NOT_EXIST` or `PERMISSION_DENIED`

**Solutions:**
```python
# Check volume permissions
# Ensure your user has CREATE and WRITE privileges on the volume

# Verify file exists locally
local_file = "./data/1_raw/myfile.csv"
print(f"File exists: {os.path.exists(local_file)}")
print(f"File size: {os.path.getsize(local_file)} bytes")

# Try uploading to DBFS instead (legacy approach)
# workspace.dbfs.upload("/FileStore/myfile.csv", open(local_file, 'rb'), overwrite=True)
```

---

#### 4. Large File Upload Timeout

**Error:** Upload times out for files >1GB

**Solutions:**
```python
# Option 1: Use Databricks CLI for large files (more reliable)
# databricks fs cp ./large_file.parquet dbfs:/Volumes/workspace/default/data/large_file.parquet

# Option 2: Split large files into chunks
import polars as pl

# For large CSV/Parquet files, split by date/chunks
df = pl.read_csv("large_file.csv")
for year in df['year'].unique():
    df_year = df.filter(pl.col('year') == year)
    df_year.write_csv(f"large_file_{year}.csv")
    # Upload each year separately
```

---

#### 5. Notebook Import Format Error

**Error:** `Error parsing notebook` or `INVALID_FORMAT`

**Solutions:**
```python
# Ensure notebook is valid JSON (for .ipynb)
import json
with open('notebook.ipynb', 'r') as f:
    try:
        nb = json.load(f)
        print("✅ Valid Jupyter notebook")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")

# Use correct import format
# For .ipynb files: ImportFormat.JUPYTER
# For .py files: ImportFormat.SOURCE or ImportFormat.PYTHON
# Let AUTO detect: ImportFormat.AUTO
```

---

## Best Practices

### 1. **Use Unity Catalog Volumes (Not DBFS)**
   - ✅ Better access control and governance
   - ✅ Supports files >2GB
   - ✅ Better organization (catalog.schema.volume hierarchy)
   - ❌ DBFS is legacy; harder to manage permissions

### 2. **Preserve Directory Structure**
   - Keep local and remote structures aligned
   - Makes debugging and navigation easier
   - Use `preserve_structure=True` in batch uploads

### 3. **Upload in Stages**
   - Upload data first (volumes)
   - Then code/notebooks (workspace)
   - Finally configs and dashboards
   - Allows testing at each stage

### 4. **Use Batch Functions for Efficiency**
   - Don't loop and upload files individually
   - Use `batch_upload_*` functions to handle errors gracefully
   - Progress tracking and summary reports included

### 5. **Version Control for Code, Volumes for Data**
   - Use Databricks Repos for `src/`, `notebooks/`, `scripts/`
   - Use Unity Catalog Volumes for `data/`, `results/`
   - Don't mix approaches

### 6. **Log Upload Activities**
   - Save upload summaries to `logs/` directory
   - Track what was uploaded when
   - Helps with troubleshooting and auditing

### 7. **Test with Small Subset First**
   - Upload 1-2 files initially to verify paths/permissions
   - Then run full batch upload
   - Avoids wasting time on misconfigurations

### 8. **Handle Sensitive Data Appropriately**
   - Never upload credentials or tokens
   - Use Databricks Secrets for sensitive configs
   - Review files before uploading

---

## Quick Reference: Complete Upload Workflow

```python
# 1. Initialize connection
from databricks.sdk import WorkspaceClient
workspace = WorkspaceClient()
current_user = workspace.current_user.me()
WORKSPACE_BASE = f"/Users/{current_user.user_name}/moh-data-analysis"

# 2. Run complete upload
upload_summary = upload_complete_project(
    catalog_name="workspace",       # Your catalog name
    schema_name="default",          # Your schema name
    project_name="moh_data_analysis" # Project identifier
)

# 3. Verify uploads
workspace_valid = verify_workspace_structure()
volumes_valid = verify_volumes()

# 4. Check results
print(f"Workspace valid: {workspace_valid}")
print(f"Volumes valid: {volumes_valid}")

# Done! Your project is now in Databricks.
```

---

## Additional Resources

- **Databricks SDK Documentation:** https://databricks-sdk-py.readthedocs.io/
- **Unity Catalog Guide:** https://docs.databricks.com/en/data-governance/unity-catalog/
- **Databricks CLI Reference:** https://docs.databricks.com/en/dev-tools/cli/
- **File API Documentation:** https://docs.databricks.com/api/workspace/files
- **Workspace API Documentation:** https://docs.databricks.com/api/workspace/workspace

---

**Last Updated:** March 2026
**Maintained by:** MOH Data Analysis Team

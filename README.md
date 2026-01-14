# nanolab_processing_base

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is a Kedro project for NanoLab data processing, generated using `kedro 0.19.10`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Quick Start

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and [DVC](https://dvc.org/) for data versioning.

### 1. Install uv (if not already installed)

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal to ensure `uv` is available:
- **macOS/Linux:** Run `source ~/.bashrc` (or `~/.zshrc`)
- **Windows:** Close and reopen PowerShell or Command Prompt

### 2. Clone the repository (if you haven't already)

**macOS/Linux/Windows:**

```bash
git clone https://github.com/YOUR_USERNAME/BTI_graphene.git
cd BTI_graphene
```

> **Windows Note:** If you don't have Git installed, download it from https://git-scm.com/download/win

### 3. Install dependencies

```bash
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install all dependencies from `pyproject.toml`
- Install the project in editable mode

> **Note:** Python 3.9 or higher is required. UV will automatically download the appropriate Python version if needed.

### 4. Configure DVC credentials (one-time setup)

The raw data is stored on [DagsHub](https://dagshub.com/tomas.rojas.c/BTI_graphene). You need to configure your DagsHub token to pull the data:

1. Create a DagsHub account at https://dagshub.com if you don't have one
2. Get your token from https://dagshub.com/user/settings/tokens
3. Configure DVC with your token:

```bash
uv run dvc remote modify --local origin access_key_id YOUR_DAGSHUB_TOKEN
uv run dvc remote modify --local origin secret_access_key YOUR_DAGSHUB_TOKEN
```

> **Note:** Both `access_key_id` and `secret_access_key` should be set to your **same** token. This creates a local configuration file (`.dvc/config.local`) that is gitignored.

### 5. Pull data with DVC

```bash
uv run dvc pull
```

This downloads the raw data (~46MB, 902 files) into `data/01_raw/`.

You can verify the download with:

```bash
uv run dvc status
```

### 6. Run the pipeline

```bash
uv run kedro run
```

This runs all pipelines. To run a specific pipeline:

```bash
uv run kedro run --pipeline=CNP_calculations
uv run kedro run --pipeline=CNP_visualizations
```

### 7. (Optional) Set up pre-commit hooks

For development, install pre-commit hooks to ensure code quality:

```bash
uv run pre-commit install
```

## Available Pipelines

| Pipeline | Description |
|----------|-------------|
| `CNP_calculations` | Charge Neutrality Point calculations |
| `CNP_visualizations` | Visualizations for CNP data |

## Common Commands

| Task | Command |
|------|---------|
| Run full pipeline | `uv run kedro run` |
| Run specific pipeline | `uv run kedro run --pipeline=<name>` |
| Visualize pipeline | `uv run kedro viz` |
| Open Jupyter Lab | `uv run kedro jupyter lab` |
| Open Jupyter Notebook | `uv run kedro jupyter notebook` |
| Open IPython with Kedro | `uv run kedro ipython` |
| Run tests | `uv run pytest` |
| Check DVC status | `uv run dvc status` |
| Add a dependency | `uv add <package-name>` |
| Add a dev dependency | `uv add --group dev <package-name>` |

## Data Version Control (DVC)

This project uses DVC to version control raw data files. The data is stored on [DagsHub](https://dagshub.com/tomas.rojas.c/BTI_graphene) and tracked via `data/01_raw.dvc`.

### Data structure

| Directory | Description |
|-----------|-------------|
| `data/01_raw/` | Raw data (tracked by DVC, stored on DagsHub) |
| `data/03_primary/` | Generated from raw data (gitignored) |
| `data/04_feature/` | Feature data (gitignored) |
| `data/05_model_input/` | Model input data (gitignored) |
| `data/06_models/` | Trained models (gitignored) |
| `data/07_model_output/` | Model outputs (gitignored) |
| `data/08_reporting/` | Reports and visualizations (gitignored) |

### Common DVC commands

```bash
# Pull data from DagsHub
uv run dvc pull

# Check data status
uv run dvc status

# Add/update raw data after changes
uv run dvc add data/01_raw
uv run dvc push

# View data pipeline
uv run dvc dag
```

## Working with Notebooks

Using `kedro jupyter` or `kedro ipython` provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.

```bash
# JupyterLab (recommended)
uv run kedro jupyter lab

# Classic Notebook
uv run kedro jupyter notebook

# IPython REPL
uv run kedro ipython
```

## Troubleshooting

### DVC pull fails with authentication error

Make sure you've configured your DagsHub token correctly:

**macOS/Linux:**

```bash
uv run dvc remote modify --local origin access_key_id YOUR_DAGSHUB_TOKEN
uv run dvc remote modify --local origin secret_access_key YOUR_DAGSHUB_TOKEN
```

**Windows (PowerShell):**

```powershell
uv run dvc remote modify --local origin access_key_id YOUR_DAGSHUB_TOKEN
uv run dvc remote modify --local origin secret_access_key YOUR_DAGSHUB_TOKEN
```

> **Windows Note:** If you get an error about `uv` not being recognized, make sure you've restarted your terminal after installing UV.

### UV sync fails

Ensure you have Python 3.9+ installed. UV will try to download a compatible Python version, but if it fails:

**Check your Python version:**

```bash
python --version
```

**Install Python if needed:**

*macOS (Homebrew):*

```bash
brew install python@3.11
```

*Windows:*

Download and install Python from https://www.python.org/downloads/

> **Windows Tip:** During installation, check "Add Python to PATH"

*Linux (Ubuntu/Debian):*

```bash
sudo apt update && sudo apt install python3.11
```

### Pipeline fails with missing data

Ensure you've pulled the data first:

```bash
uv run dvc pull
uv run dvc status  # Should show no changes
```

## Rules and Guidelines

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data directly to your repository — use DVC instead
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

### Windows-specific issues

**Long path errors:**

If you encounter errors related to long file paths on Windows, enable long paths:

1. Open PowerShell as Administrator
2. Run:

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

3. Restart your computer

**Permission errors:**

If you get permission errors, try running PowerShell as Administrator, or check that your antivirus isn't blocking the operation.

**Line ending issues:**

Configure Git to handle line endings correctly:

```bash
git config --global core.autocrlf true
```

## Further Reading

- [Kedro Documentation](https://docs.kedro.org)
- [UV Documentation](https://docs.astral.sh/uv/)
- [DVC Documentation](https://dvc.org/doc)
- [DagsHub Documentation](https://dagshub.com/docs/)

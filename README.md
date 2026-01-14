# nanolab_processing_base

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is a Kedro project for NanoLab data processing, generated using `kedro 0.19.10`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Quick Start

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and [DVC](https://dvc.org/) for data versioning.

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies

```bash
uv sync
```

This will create a virtual environment and install all dependencies.

### 3. Pull data with DVC

```bash
uv run dvc pull
```

This downloads the tracked data files from the remote storage.

### 4. Run the pipeline

```bash
uv run kedro run
```

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data directly to your repository — use DVC instead
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## Data Version Control (DVC)

This project uses DVC to version control data files. The data is stored remotely and tracked via `data.dvc`.

### Common DVC commands

```bash
# Pull data from remote storage
uv run dvc pull

# Check data status
uv run dvc status

# Add/update data after changes
uv run dvc add data
uv run dvc push

# View data pipeline
uv run dvc dag
```

### Setting up a remote storage

To push data, you need to configure a DVC remote. For example, with S3:

```bash
uv run dvc remote add -d myremote s3://mybucket/path
```

Or with a local/network path:

```bash
uv run dvc remote add -d myremote /path/to/remote/storage
```

## How to run your Kedro pipeline

```bash
uv run kedro run
```

Run specific pipelines:

```bash
uv run kedro run --pipeline=CNP_calculations
uv run kedro run --pipeline=CNP_visualizations
```

## How to test your Kedro project

```bash
uv run pytest
```

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.

### Jupyter/JupyterLab

```bash
uv run kedro jupyter notebook
# or
uv run kedro jupyter lab
```

### IPython

```bash
uv run kedro ipython
```

## Visualize the pipeline

```bash
uv run kedro viz
```

## Project dependencies

Dependencies are managed in `pyproject.toml`. To add a new dependency:

```bash
uv add <package-name>
```

To add a dev dependency:

```bash
uv add --group dev <package-name>
```

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)

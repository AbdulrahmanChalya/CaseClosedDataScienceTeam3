# CaseClosed

Basic data science workspace.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
export MPLCONFIGDIR=.cache/matplotlib
export XDG_CACHE_HOME=.cache
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name caseclosed --display-name "Python (CaseClosed)"
```

## Start JupyterLab

```bash
source .venv/bin/activate
export MPLCONFIGDIR=.cache/matplotlib
export XDG_CACHE_HOME=.cache
jupyter lab
```

Use the `Python (CaseClosed)` kernel in notebooks.

## Project layout

- `notebooks/`: exploratory notebooks
- `src/`: reusable Python code
- `data/raw/`: original local data files
- `data/interim/`: temporary transformed data
- `data/processed/`: final analysis-ready data
- `models/`: trained model artifacts
- `reports/`: generated outputs

The local data and artifact folders are ignored by Git by default.

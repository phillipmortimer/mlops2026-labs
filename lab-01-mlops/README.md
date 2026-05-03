# Lab 01: MLOps Foundations with MLflow

This lab introduces the operational basics of classical MLOps:

- reproducible training runs
- experiment tracking
- run comparison
- model registration
- simple local inference

The starter project uses the built-in scikit-learn `digits` dataset, so there is no separate dataset download step.

## Prerequisites

You need `uv`, a Python project and environment manager.

Install `uv` with the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal or follow the installer message to update your `PATH`, then check:

```bash
uv --version
```

Reference: https://docs.astral.sh/uv/getting-started/installation/

## Learning goals

By the end of the lab, students should be able to:

- run a baseline supervised training workflow
- add `MLflow` experiment tracking
- log parameters, metrics, and artifacts
- compare multiple model types and runs
- register a selected model
- use the trained model for simple local inference

## Project structure

```text
lab-01-mlops/
├── README.md
├── pyproject.toml
├── configs/
│   ├── baseline.json
│   ├── mlp.json
│   ├── random_forest.json
│   └── svm.json
└── src/
    ├── predict.py
    └── train.py
```

## Setup

From this lab directory, install the project dependencies:

```bash
uv sync
```

This creates a local `.venv` and installs everything listed in `pyproject.toml`, including:

- `scikit-learn`
- `joblib`
- `mlflow`

You do not need to install `MLflow` separately. Check that it is available with:

```bash
uv run mlflow --version
```

## Run the baseline training job

The starter code already trains a simple classifier and writes local artifacts:

```bash
uv run python src/train.py --config configs/baseline.json
```

The baseline config trains a logistic regression classifier.

This will create:

- `artifacts/model.joblib`
- `artifacts/metrics.json`
- `artifacts/test_predictions.csv`
- `artifacts/classification_report.json`

## View MLflow runs

Once you have added MLflow tracking and run the training script, start the local MLflow UI:

```bash
uv run mlflow ui
```

Then open:

```text
http://127.0.0.1:5000
```

## Run local inference

```bash
uv run python src/predict.py --model-path artifacts/model.joblib --sample-index 0
```

## Student tasks

The baseline runs without `MLflow`. Your task is to add it.

### Task 1
Create an MLflow experiment and log:

- parameters from the config file
- train/test split metadata
- the model type and model-specific settings
- accuracy and macro F1
- the trained model as an artifact

### Task 2
Run several model variants and compare them in MLflow. Example configs are provided:

```bash
uv run python src/train.py --config configs/baseline.json
uv run python src/train.py --config configs/random_forest.json
uv run python src/train.py --config configs/svm.json
uv run python src/train.py --config configs/mlp.json
```

You can also create your own config by changing model type or model-specific settings.

Compare the runs in MLflow and identify the best candidate. Consider both performance and operational tradeoffs such as training time, model simplicity, and reproducibility.

### Task 3
Register the selected model in MLflow with a meaningful model name.

Suggested model name:
- `pdpsl-digits-classifier`

### Task 4
Keep the local inference script working with the saved model artifact.

### Optional extension
Create a small prediction viewer for the digits dataset.

The viewer should:

- load a saved model from `artifacts/model.joblib`
- display at least 10 digit images from the built-in scikit-learn dataset
- show the predicted class next to the true label
- clearly mark correct and incorrect predictions
- run from the command line

Example command:

```bash
uv run python src/view_predictions.py --model-path artifacts/model.joblib --count 12
```

You may choose the output format. For example, the viewer could open a local plot window, write an image file, or generate a small HTML page.

## Suggested workflow

1. Run the baseline code once without modifications
2. Read the TODO comments in `src/train.py`
3. Add MLflow tracking
4. Run multiple model variants
5. Register the best model
6. Verify local inference still works

## Deliverables

Students should be able to show:

- at least two tracked MLflow runs
- logged parameters and metrics
- a registered model version
- a working local prediction script
- a short explanation of why one model type was chosen over another

Optional extension deliverable:

- a prediction viewer showing sample digit images, predicted labels, true labels, and which examples were misclassified

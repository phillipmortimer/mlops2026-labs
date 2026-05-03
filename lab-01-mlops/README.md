# Lab 01: MLOps Foundations with MLflow

This lab introduces the operational basics of classical MLOps:

- reproducible training runs
- experiment tracking
- run comparison
- model registration
- simple local inference

The starter project uses the built-in scikit-learn `digits` dataset, so there is no separate dataset download step.

## Learning goals

By the end of the lab, students should be able to:

- run a baseline supervised training workflow
- add `MLflow` experiment tracking
- log parameters, metrics, and artifacts
- compare multiple runs
- register a selected model
- use the trained model for simple local inference

## Project structure

```text
lab-01-mlops/
├── README.md
├── pyproject.toml
├── configs/
│   └── baseline.json
└── src/
    ├── predict.py
    └── train.py
```

## Setup with uv

```bash
uv sync
```

## Run the baseline training job

The starter code already trains a simple classifier and writes local artifacts.

```bash
uv run python src/train.py --config configs/baseline.json
```

This will create:

- `artifacts/model.joblib`
- `artifacts/metrics.json`
- `artifacts/test_predictions.csv`
- `artifacts/classification_report.json`

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
- accuracy and macro F1
- the trained model as an artifact

### Task 2
Run at least two variants by changing one or more hyperparameters, for example:

- `C`
- `max_iter`
- `test_size`

Compare the runs in MLflow and identify the best candidate.

### Task 3
Register the selected model in MLflow with a meaningful model name.

Suggested model name:
- `pdpsl-digits-classifier`

### Task 4
Keep the local inference script working with the saved model artifact.

## Suggested workflow

1. Run the baseline code once without modifications
2. Read the TODO comments in `src/train.py`
3. Add MLflow tracking
4. Run multiple experiments
5. Register the best model
6. Verify local inference still works

## Deliverables

Students should be able to show:

- at least two tracked MLflow runs
- logged parameters and metrics
- a registered model version
- a working local prediction script
- a short explanation of why one run was chosen over another

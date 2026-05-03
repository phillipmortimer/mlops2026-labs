from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import joblib
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


ARTIFACTS_DIR = Path("artifacts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a digits classifier.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/baseline.json"),
        help="Path to the training config JSON file.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_data() -> tuple:
    dataset = load_digits()
    return dataset.data, dataset.target


def build_model(config: dict):
    model_config = config["model"]
    model_type = model_config["type"]

    if model_type == "logistic_regression":
        return LogisticRegression(
            C=model_config["C"],
            max_iter=model_config["max_iter"],
            solver=model_config["solver"],
        )

    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=model_config["n_estimators"],
            max_depth=model_config.get("max_depth"),
            random_state=config["random_state"],
        )

    if model_type == "svm":
        return SVC(
            C=model_config["C"],
            kernel=model_config["kernel"],
            gamma=model_config["gamma"],
        )

    if model_type == "mlp":
        return MLPClassifier(
            hidden_layer_sizes=tuple(model_config["hidden_layer_sizes"]),
            activation=model_config["activation"],
            learning_rate_init=model_config["learning_rate_init"],
            max_iter=model_config["max_iter"],
            random_state=config["random_state"],
        )

    raise ValueError(f"Unsupported model type: {model_type}")


def save_predictions(output_path: Path, predictions: list[int], labels: list[int]) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["prediction", "label"])
        writer.writerows(zip(predictions, labels))


def save_json(output_path: Path, payload: dict) -> None:
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    features, labels = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=config["test_size"],
        random_state=config["random_state"],
        stratify=labels,
    )

    model = build_model(config)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")
    report = classification_report(y_test, predictions, output_dict=True)

    metrics = {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "test_examples": len(y_test),
    }

    model_path = ARTIFACTS_DIR / "model.joblib"
    metrics_path = ARTIFACTS_DIR / "metrics.json"
    predictions_path = ARTIFACTS_DIR / "test_predictions.csv"
    report_path = ARTIFACTS_DIR / "classification_report.json"

    joblib.dump(model, model_path)
    save_json(metrics_path, metrics)
    save_json(report_path, report)
    save_predictions(predictions_path, predictions.tolist(), y_test.tolist())

    print("Training complete.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")

    # TODO(student): import mlflow and set the experiment name.
    # Suggested value: config["experiment_name"]

    # TODO(student): wrap the train/evaluate workflow in an MLflow run.

    # TODO(student): log parameters such as test_size, random_state, model.type,
    # and the model-specific settings from config["model"].

    # TODO(student): log metrics such as accuracy, macro_f1, and test_examples.

    # TODO(student): log local artifacts such as metrics.json, classification_report.json,
    # test_predictions.csv, and the trained model file.

    # TODO(student): register the trained model in MLflow using the config value
    # config["register_model_name"] once you have selected a candidate version.


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
from sklearn.datasets import load_digits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local inference with a saved digits model.")
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path("artifacts/model.joblib"),
        help="Path to the saved model.",
    )
    parser.add_argument(
        "--sample-index",
        type=int,
        default=0,
        help="Index of the sample to predict.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = joblib.load(args.model_path)

    dataset = load_digits()
    sample = dataset.data[args.sample_index].reshape(1, -1)
    label = dataset.target[args.sample_index]
    prediction = model.predict(sample)[0]

    print(f"Sample index: {args.sample_index}")
    print(f"Predicted label: {prediction}")
    print(f"True label: {label}")


if __name__ == "__main__":
    main()

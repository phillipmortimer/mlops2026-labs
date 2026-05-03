from __future__ import annotations

import argparse
import csv
import json
import random
import urllib.request
from pathlib import Path


DATASET_URL = (
    "https://huggingface.co/datasets/bitext/"
    "Bitext-customer-support-llm-chatbot-training-dataset/resolve/main/"
    "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)
RAW_FILENAME = "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
DEFAULT_SUPPORT_SIZE = 60
DEFAULT_EVAL_SIZE = 20
DEFAULT_SEED = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and prepare the Bitext customer-support dataset."
    )
    parser.add_argument(
        "--support-size",
        type=int,
        default=DEFAULT_SUPPORT_SIZE,
        help="Number of support examples to write.",
    )
    parser.add_argument(
        "--eval-size",
        type=int,
        default=DEFAULT_EVAL_SIZE,
        help="Number of eval examples to write.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed for deterministic sampling.",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Download the source CSV even if it already exists.",
    )
    return parser.parse_args()


def download_dataset(raw_path: Path, force_download: bool) -> None:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists() and not force_download:
        print(f"Using existing source CSV: {raw_path}")
        return

    print(f"Downloading Bitext dataset from: {DATASET_URL}")
    urllib.request.urlretrieve(DATASET_URL, raw_path)
    print(f"Saved source CSV to: {raw_path}")


def load_rows(raw_path: Path) -> list[dict]:
    with raw_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            instruction = row.get("instruction", "")
            has_required_labels = row.get("category") and row.get("intent")
            has_template_placeholder = "{{" in instruction or "}}" in instruction
            if instruction and has_required_labels and not has_template_placeholder:
                rows.append(row)
    return rows


def normalize_row(row: dict, example_id: str) -> dict:
    return {
        "id": example_id,
        "instruction": row["instruction"].strip(),
        "category": row["category"].strip(),
        "intent": row["intent"].strip(),
        "reference_response": row.get("response", "").strip(),
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()

    lab_dir = Path(__file__).resolve().parents[1]
    data_dir = lab_dir / "data"
    raw_path = data_dir / "raw" / RAW_FILENAME

    download_dataset(raw_path, args.force_download)
    rows = load_rows(raw_path)

    required_rows = args.support_size + args.eval_size
    if len(rows) < required_rows:
        raise ValueError(
            f"Dataset only has {len(rows)} usable rows; requested {required_rows}."
        )

    rng = random.Random(args.seed)
    sampled_rows = rng.sample(rows, required_rows)

    support_rows = [
        normalize_row(row, f"support-{index:03d}")
        for index, row in enumerate(sampled_rows[: args.support_size], start=1)
    ]
    eval_rows = [
        normalize_row(row, f"eval-{index:03d}")
        for index, row in enumerate(sampled_rows[args.support_size :], start=1)
    ]

    support_path = data_dir / "support_tickets.jsonl"
    eval_path = data_dir / "eval_set.jsonl"

    write_jsonl(support_path, support_rows)
    write_jsonl(eval_path, eval_rows)

    print(f"Wrote {len(support_rows)} support examples to: {support_path}")
    print(f"Wrote {len(eval_rows)} eval examples to: {eval_path}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def find_example(examples: list[dict], example_id: str) -> dict:
    for example in examples:
        if example["id"] == example_id:
            return example
    raise ValueError(f"Could not find example with id: {example_id}")


def available_labels(examples: list[dict]) -> tuple[list[str], list[str]]:
    categories = sorted({example["category"] for example in examples})
    intents = sorted({example["intent"] for example in examples})
    return categories, intents


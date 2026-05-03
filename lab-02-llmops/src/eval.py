from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

from data import available_labels, load_jsonl
from triage import load_config, mock_triage, triage_ticket


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate support triage on a fixed set.")
    parser.add_argument(
        "--eval-path",
        type=Path,
        default=Path("data/eval_set.jsonl"),
        help="Path to prepared eval examples.",
    )
    parser.add_argument(
        "--label-source-path",
        type=Path,
        default=Path("data/support_tickets.jsonl"),
        help="Path used to infer allowed category and intent labels.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("outputs/eval_results.jsonl"),
        help="Where to write per-example outputs.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit for quick checks.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model override. Defaults to OPENAI_MODEL from .env.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use deterministic mock output instead of calling the OpenAI API.",
    )
    return parser.parse_args()


def score_output(example: dict, output: dict) -> dict:
    return {
        "category_correct": output.get("category") == example["category"],
        "intent_correct": output.get("intent") == example["intent"],
        "valid_priority": output.get("priority") in {"low", "normal", "high", "urgent"},
    }


def main() -> None:
    args = parse_args()
    eval_examples = load_jsonl(args.eval_path)
    label_examples = load_jsonl(args.label_source_path) + eval_examples
    categories, intents = available_labels(label_examples)
    config = load_config(args.model)

    if args.limit is not None:
        eval_examples = eval_examples[: args.limit]

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    results = []
    started = perf_counter()

    with args.output_path.open("w", encoding="utf-8") as handle:
        for example in eval_examples:
            item_started = perf_counter()
            if args.mock:
                output = mock_triage(example["instruction"], categories, intents)
            else:
                output = triage_ticket(example["instruction"], categories, intents, config)
            latency_seconds = perf_counter() - item_started
            scores = score_output(example, output)
            result = {
                "id": example["id"],
                "instruction": example["instruction"],
                "expected_category": example["category"],
                "expected_intent": example["intent"],
                "model": config.model,
                "group_id": config.group_id,
                "latency_seconds": round(latency_seconds, 4),
                "output": output,
                "scores": scores,
            }
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")

            # TODO(student): log per-example eval results to Langfuse.
            # Include example id, expected labels, predicted labels, scores,
            # model, prompt version, group id, and latency.

    total = len(results)
    category_accuracy = sum(item["scores"]["category_correct"] for item in results) / total
    intent_accuracy = sum(item["scores"]["intent_correct"] for item in results) / total
    valid_priority_rate = sum(item["scores"]["valid_priority"] for item in results) / total
    elapsed = perf_counter() - started

    print("Evaluation complete.")
    print(f"Examples: {total}")
    print(f"Category accuracy: {category_accuracy:.3f}")
    print(f"Intent accuracy: {intent_accuracy:.3f}")
    print(f"Valid priority rate: {valid_priority_rate:.3f}")
    print(f"Elapsed seconds: {elapsed:.2f}")
    print(f"Results written to: {args.output_path}")


if __name__ == "__main__":
    main()

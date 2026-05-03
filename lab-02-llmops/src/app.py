from __future__ import annotations

import argparse
import json
from pathlib import Path

from data import available_labels, find_example, load_jsonl
from triage import load_config, mock_triage, triage_ticket


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run support triage for one ticket.")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("data/support_tickets.jsonl"),
        help="Path to prepared support examples.",
    )
    parser.add_argument(
        "--ticket-id",
        default="support-001",
        help="Ticket id to triage.",
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


def main() -> None:
    args = parse_args()
    examples = load_jsonl(args.data_path)
    categories, intents = available_labels(examples)
    ticket = find_example(examples, args.ticket_id)
    config = load_config(args.model)

    if args.mock:
        output = mock_triage(ticket["instruction"], categories, intents)
    else:
        output = triage_ticket(ticket["instruction"], categories, intents, config)

    result = {
        "ticket_id": ticket["id"],
        "instruction": ticket["instruction"],
        "expected_category": ticket["category"],
        "expected_intent": ticket["intent"],
        "model": config.model,
        "group_id": config.group_id,
        "output": output,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # TODO(student): instrument this request with Langfuse.
    # Capture ticket_id, group_id, prompt_version, model, input, output,
    # expected labels, latency, token usage, and any eval metadata available.


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import sys

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "plugins" / "support-ops"
sys.path.append(str(PLUGIN_DIR / "tools"))

from support_tools import (  # noqa: E402
    draft_refund_request,
    lookup_customer,
    lookup_order,
    submit_refund_request,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the support-ops task suite.")
    parser.add_argument(
        "--tasks-path",
        type=Path,
        default=Path("tasks/support_tasks.jsonl"),
        help="Path to the fixed task suite.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("trajectories/baseline.jsonl"),
        help="Where to write trajectory records.",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def find_identifier(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(0)


def tool_result_payload(result) -> dict:
    return {
        "ok": result.ok,
        "message": result.message,
        "data": result.data,
    }


def run_task(task: dict) -> dict:
    goal = task["goal"]
    customer_id = find_identifier(r"cust-\d+", goal)
    order_id = find_identifier(r"ord-\d+", goal)
    approval_code = find_identifier(r"APPROVE-\d+", goal)
    steps = []

    if customer_id:
        result = lookup_customer(customer_id)
        steps.append(
            {
                "step": len(steps) + 1,
                "tool": "lookup_customer",
                "arguments": {"customer_id": customer_id},
                "result": tool_result_payload(result),
            }
        )

    if order_id:
        result = lookup_order(order_id)
        steps.append(
            {
                "step": len(steps) + 1,
                "tool": "lookup_order",
                "arguments": {"order_id": order_id},
                "result": tool_result_payload(result),
            }
        )

    if not order_id:
        return {
            "task_id": task["id"],
            "plugin": "support-ops",
            "skill": "support-ops",
            "goal": goal,
            "steps": steps,
            "stop_reason": "missing_required_identifier",
            "final_outcome": "Ask the user for the missing customer id and order id.",
        }

    if "refund" in goal.lower() and not approval_code:
        result = draft_refund_request(order_id, "Customer requested refund.")
        steps.append(
            {
                "step": len(steps) + 1,
                "tool": "draft_refund_request",
                "arguments": {"order_id": order_id, "reason": "Customer requested refund."},
                "result": tool_result_payload(result),
            }
        )
        return {
            "task_id": task["id"],
            "plugin": "support-ops",
            "skill": "support-ops",
            "goal": goal,
            "steps": steps,
            "approval_required": True,
            "stop_reason": "approval_required",
            "final_outcome": "Prepared a draft where possible and stopped before submission.",
        }

    if approval_code:
        result = submit_refund_request(
            order_id,
            "Approved refund request.",
            approval_code,
        )
        steps.append(
            {
                "step": len(steps) + 1,
                "tool": "submit_refund_request",
                "arguments": {
                    "order_id": order_id,
                    "reason": "Approved refund request.",
                    "approval_code": approval_code,
                },
                "result": tool_result_payload(result),
            }
        )
        return {
            "task_id": task["id"],
            "plugin": "support-ops",
            "skill": "support-ops",
            "goal": goal,
            "steps": steps,
            "approval_required": True,
            "stop_reason": "completed_with_approval",
            "final_outcome": "Submitted the refund request using the provided approval code.",
        }

    return {
        "task_id": task["id"],
        "plugin": "support-ops",
        "skill": "support-ops",
        "goal": goal,
        "steps": steps,
        "stop_reason": "no_action_needed",
        "final_outcome": "No sensitive action was taken.",
    }


def main() -> None:
    args = parse_args()
    tasks = load_jsonl(args.tasks_path)
    args.output_path.parent.mkdir(parents=True, exist_ok=True)

    trajectories = [run_task(task) for task in tasks]
    with args.output_path.open("w", encoding="utf-8") as handle:
        for trajectory in trajectories:
            handle.write(json.dumps(trajectory, ensure_ascii=False) + "\n")

    print(f"Wrote {len(trajectories)} trajectories to: {args.output_path}")
    for trajectory in trajectories:
        print(
            f"{trajectory['task_id']}: {trajectory['stop_reason']} "
            f"({len(trajectory['steps'])} steps)"
        )


if __name__ == "__main__":
    main()


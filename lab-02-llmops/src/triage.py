from __future__ import annotations

import json
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from prompts import BASELINE_PROMPT_VERSION, build_system_prompt, build_user_prompt


TRIAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "description": "The support category selected from the allowed category labels.",
        },
        "intent": {
            "type": "string",
            "description": "The customer intent selected from the allowed intent labels.",
        },
        "priority": {
            "type": "string",
            "enum": ["low", "normal", "high", "urgent"],
            "description": "The operational priority for handling the ticket.",
        },
        "draft_response": {
            "type": "string",
            "description": "A concise first response to the customer.",
        },
        "rationale": {
            "type": "string",
            "description": "One short sentence explaining the classification.",
        },
    },
    "required": ["category", "intent", "priority", "draft_response", "rationale"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class TriageConfig:
    model: str
    group_id: str
    prompt_version: str = BASELINE_PROMPT_VERSION


def load_config(model_override: str | None = None) -> TriageConfig:
    load_dotenv()
    return TriageConfig(
        model=model_override or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        group_id=os.getenv("GROUP_ID", "unknown-group"),
    )


def mock_triage(instruction: str, categories: list[str], intents: list[str]) -> dict:
    lowered = instruction.lower()
    category = categories[0]
    intent = intents[0]

    keyword_rules = [
        ("refund", "REFUND", "check_refund_policy"),
        ("reimburse", "REFUND", "check_refund_policy"),
        ("cancel", "CANCEL", "check_cancellation_fee"),
        ("delivery", "DELIVERY", "delivery_options"),
        ("shipping", "SHIPPING", "change_shipping_address"),
        ("account", "ACCOUNT", "create_account"),
        ("feedback", "FEEDBACK", "review"),
    ]
    for keyword, rule_category, rule_intent in keyword_rules:
        if keyword in lowered:
            if rule_category in categories:
                category = rule_category
            if rule_intent in intents:
                intent = rule_intent
            break

    return {
        "category": category,
        "intent": intent,
        "priority": "normal",
        "draft_response": "Thanks for contacting support. I can help with this request and will guide you through the next step.",
        "rationale": "Keyword-based mock output for local testing without an API call.",
    }


def triage_ticket(
    instruction: str,
    categories: list[str],
    intents: list[str],
    config: TriageConfig,
) -> dict:
    client = OpenAI()
    try:
        response = client.responses.create(
            model=config.model,
            input=[
                {"role": "system", "content": build_system_prompt(categories, intents)},
                {"role": "user", "content": build_user_prompt(instruction)},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "support_triage",
                    "schema": TRIAGE_SCHEMA,
                    "strict": True,
                }
            },
        )
    except OpenAIError as exc:
        raise RuntimeError(
            f"OpenAI request failed for model {config.model!r}. "
            "Check OPENAI_API_KEY, project access, model access, and organization verification. "
            "For new accounts, try OPENAI_MODEL=gpt-4o-mini."
        ) from exc
    return json.loads(response.output_text)

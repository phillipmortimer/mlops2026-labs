---
name: support-ops
description: Use this skill for bounded customer-support operations over local mock customer and order records. The skill can inspect account/order state, draft refund requests, and request approval for sensitive actions.
---

# Support Operations Skill

## Goal

Help with customer-support operations using only the local tools exposed by the `support-ops` plugin.

## Available Tools

- `lookup_customer(customer_id)`: read-only customer lookup.
- `lookup_order(order_id)`: read-only order lookup.
- `draft_refund_request(order_id, reason)`: creates a draft refund request. This does not submit anything.
- `submit_refund_request(order_id, reason, approval_code)`: submits a refund request. This is sensitive.

## Operating Rules

- Use read-only lookup tools before drafting or submitting any refund action.
- Never invent customer, account, order, payment, shipping, or refund details.
- If required identifiers are missing, stop and ask for the missing information.
- Drafting a refund request is allowed when the order exists and the reason is clear.
- Submitting a refund request requires explicit approval.
- If approval is missing, stop after preparing the draft and ask for approval.
- Prefer a safe stop over an overconfident action.

## Output Expectations

For each task, produce:

- a concise summary of what was checked
- the action taken or recommended
- whether approval was required
- the stop reason

## Known Weakness To Investigate

This first version may not be strict enough about approval boundaries. Inspect trajectories carefully and improve this skill if sensitive actions are taken too early.


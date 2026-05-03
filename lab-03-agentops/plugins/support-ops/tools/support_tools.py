from __future__ import annotations

from dataclasses import dataclass


CUSTOMERS = {
    "cust-1001": {
        "name": "Ari Martin",
        "tier": "standard",
        "status": "active",
    },
    "cust-1002": {
        "name": "Bea Chen",
        "tier": "pro",
        "status": "active",
    },
}


ORDERS = {
    "ord-9001": {
        "customer_id": "cust-1001",
        "status": "delivered",
        "amount": 49.99,
        "eligible_for_refund": True,
    },
    "ord-9002": {
        "customer_id": "cust-1002",
        "status": "shipped",
        "amount": 129.0,
        "eligible_for_refund": False,
    },
}


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    message: str
    data: dict


def lookup_customer(customer_id: str) -> ToolResult:
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return ToolResult(False, "Customer not found.", {"customer_id": customer_id})
    return ToolResult(True, "Customer found.", {"customer_id": customer_id, **customer})


def lookup_order(order_id: str) -> ToolResult:
    order = ORDERS.get(order_id)
    if order is None:
        return ToolResult(False, "Order not found.", {"order_id": order_id})
    return ToolResult(True, "Order found.", {"order_id": order_id, **order})


def draft_refund_request(order_id: str, reason: str) -> ToolResult:
    order = ORDERS.get(order_id)
    if order is None:
        return ToolResult(False, "Cannot draft refund for an unknown order.", {"order_id": order_id})
    if not order["eligible_for_refund"]:
        return ToolResult(
            False,
            "Order is not eligible for an automatic refund draft.",
            {"order_id": order_id, "eligible_for_refund": False},
        )
    return ToolResult(
        True,
        "Refund request drafted. Approval is required before submission.",
        {"order_id": order_id, "reason": reason, "status": "draft"},
    )


def submit_refund_request(order_id: str, reason: str, approval_code: str | None) -> ToolResult:
    if not approval_code:
        return ToolResult(
            False,
            "Approval code is required before submitting a refund request.",
            {"order_id": order_id, "submitted": False},
        )
    draft = draft_refund_request(order_id, reason)
    if not draft.ok:
        return draft
    return ToolResult(
        True,
        "Refund request submitted.",
        {"order_id": order_id, "reason": reason, "approval_code": approval_code, "submitted": True},
    )


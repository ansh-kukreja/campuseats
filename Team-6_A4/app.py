from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from flask import Flask, jsonify, request

from errors import ProblemError, problem, register_error_handlers
from models import Order, OrderItem
from payment_client import PaymentClient, PaymentRejected, PaymentUnavailable
from store import OrderStore


app = Flask(__name__)
store = OrderStore()
payment_client: PaymentClient | None = None
register_error_handlers(app)

VALID_STATUSES = {"PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"}


def get_payment_client() -> PaymentClient:
    global payment_client
    if payment_client is None:
        payment_client = PaymentClient()
    return payment_client


def validate(body: Any, idempotency_key: str | None) -> None:
    """
    Manual request validation.

    This replaces the XML Schema validation that Assignment 3 provided before
    the SOAP operation executed.
    """
    if not isinstance(body, dict):
        raise ProblemError(
            400, "Bad request", "Request body must be a JSON object.", "bad-request"
        )

    if not idempotency_key or not idempotency_key.strip():
        raise ProblemError(
            400,
            "Bad request",
            "Idempotency-Key header is required.",
            "bad-request",
        )

    student_id = body.get("studentId")
    if not isinstance(student_id, str) or not student_id.strip():
        raise ProblemError(
            400, "Bad request", "studentId is required.", "bad-request"
        )

    items = body.get("items")
    if not isinstance(items, list) or not items:
        raise ProblemError(
            400,
            "Bad request",
            "items must be a non-empty array.",
            "bad-request",
        )

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}] must be an object.",
                "bad-request",
            )

        item_id = item.get("itemId")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}].itemId is required.",
                "bad-request",
            )

        quantity = item.get("quantity")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}].quantity must be a positive integer.",
                "bad-request",
            )

        # unitPrice is retained as a simple in-process representation of the
        # catalogue price for this assignment. In a production system it would
        # be obtained from the Catalogue service, not trusted from the client.
        unit_price = item.get("unitPrice")
        if unit_price is None:
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}].unitPrice is required.",
                "bad-request",
            )
        try:
            price = Decimal(str(unit_price))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}].unitPrice must be numeric.",
                "bad-request",
            ) from exc

        if price < 0:
            raise ProblemError(
                400,
                "Bad request",
                f"items[{index}].unitPrice cannot be negative.",
                "bad-request",
            )

    payment_method = body.get("paymentMethod")
    if not isinstance(payment_method, str) or not payment_method.strip():
        raise ProblemError(
            400, "Bad request", "paymentMethod is required.", "bad-request"
        )


def fingerprint(body: dict[str, Any]) -> str:
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def parse_items(body: dict[str, Any]) -> list[OrderItem]:
    return [
        OrderItem(
            item_id=item["itemId"],
            quantity=item["quantity"],
            unit_price=Decimal(str(item["unitPrice"])),
        )
        for item in body["items"]
    ]


def create_order(body: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
    validate(body, idempotency_key)

    request_hash = fingerprint(body)
    existing = store.find_by_idempotency_key(idempotency_key)
    if existing is not None:
        if existing.request_fingerprint != request_hash:
            raise ProblemError(
                409,
                "Idempotency key conflict",
                "The same Idempotency-Key was already used with a different request.",
                "idempotency-conflict",
            )
        return existing.as_json()

    items = parse_items(body)
    total = sum((item.line_total for item in items), Decimal("0.00"))

    # A valid request can still be refused by the domain.
    if total <= 0:
        raise ProblemError(
            422,
            "Order refused",
            "The order total must be greater than zero.",
            "order-refused",
        )

    order_id = store.next_id()

    try:
        get_payment_client().charge(
            order_id=order_id,
            amount=float(total),
            payment_method=body["paymentMethod"],
            idempotency_key=idempotency_key,
        )
    except PaymentRejected as exc:
        raise ProblemError(
            422,
            "Payment declined",
            str(exc),
            "payment-declined",
        ) from exc
    except PaymentUnavailable as exc:
        raise ProblemError(
            503,
            "Payment service unavailable",
            str(exc),
            "payment-unavailable",
        ) from exc

    order = Order(
        internal_id=str(uuid.uuid4()),
        order_id=order_id,
        student_id=body["studentId"],
        items=items,
        payment_method=body["paymentMethod"],
        total=total,
        status="PENDING",
        estimated_ready_minutes=15,
        idempotency_key=idempotency_key,
        request_fingerprint=request_hash,
        _created_at=datetime.now(timezone.utc).isoformat(),
    )
    store.save(order)
    return order.as_json()


@app.post("/orders")
def post_order():
    body = request.get_json(silent=True)
    key = request.headers.get("Idempotency-Key")

    response_body = create_order(body, key)

    # Location is required on successful creation. If the response came from
    # an idempotent repeat, it is still the original resource.
    location = f"/orders/{response_body['orderId']}"
    response = jsonify(response_body)
    response.status_code = 201
    response.headers["Location"] = location
    return response


@app.get("/orders/<int:order_id>")
def get_order(order_id: int):
    order = store.find_by_id(order_id)
    if order is None:
        raise ProblemError(
            404,
            "Order not found",
            f"No order exists with id {order_id}.",
            "order-not-found",
        )
    return jsonify(order.as_json()), 200


@app.get("/orders")
def list_orders():
    student_id = request.args.get("studentId")
    status = request.args.get("status")

    if student_id is not None and not student_id.strip():
        raise ProblemError(
            400, "Bad request", "studentId cannot be blank.", "bad-request"
        )

    if status is not None:
        status = status.upper()
        if status not in VALID_STATUSES:
            raise ProblemError(
                400,
                "Bad request",
                f"Unknown order status: {status}.",
                "bad-request",
            )

    orders = store.find_all(student_id=student_id, status=status)
    return jsonify([order.as_json() for order in orders]), 200


@app.post("/orders/<int:order_id>/cancellation")
def cancel_order(order_id: int):
    order = store.find_by_id(order_id)
    if order is None:
        raise ProblemError(
            404,
            "Order not found",
            f"No order exists with id {order_id}.",
            "order-not-found",
        )

    if order.status in {"CANCELLED", "COMPLETED"}:
        raise ProblemError(
            409,
            "Order state conflict",
            f"Order {order_id} cannot be cancelled from state {order.status}.",
            "order-conflict",
        )

    order.status = "CANCELLED"
    store.save(order)
    return jsonify(order.as_json()), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

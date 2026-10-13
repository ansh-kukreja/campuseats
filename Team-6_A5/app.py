from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from functools import wraps
from typing import Any

from flask import Flask, jsonify, make_response, request

from errors import ProblemError, problem
from models import Order, OrderItem
from store import OrderStore
from payment_client import PaymentClient, PaymentRejected, PaymentUnavailable


def create_app(payment_charge=None):
    app = Flask(__name__)
    store = OrderStore()
    payment = PaymentClient(charge=payment_charge)

    # Demo token is intentionally non-secret. It demonstrates header handling.
    DEMO_TOKEN = os.getenv("DEMO_BEARER_TOKEN", "demo-token")
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "10"))
    RATE_WINDOW = 60.0
    rate_state = defaultdict(deque)

    def json_response(data, status=200, headers=None):
        response = make_response(jsonify(data), status)
        if headers:
            for k, v in headers.items():
                response.headers[k] = v
        return response

    def fail(status, title, detail, kind="bad-request"):
        raise ProblemError(status, title, detail, kind)

    @app.errorhandler(ProblemError)
    def handle_problem(exc):
        return problem(exc.status, exc.title, exc.detail, exc.kind, exc.extra_headers)

    @app.errorhandler(404)
    def handle_404(_):
        return problem(404, "Not found", "The requested resource does not exist.", "not-found")

    @app.errorhandler(405)
    def handle_405(_):
        return problem(405, "Method not allowed", "Use OPTIONS to discover the methods allowed for this resource.", "method-not-allowed", extra_headers={"Allow": "GET, POST, PUT, OPTIONS"})

    @app.errorhandler(415)
    def handle_415(_):
        return problem(415, "Unsupported media type", "Use application/json for request bodies.", "unsupported-media-type")

    @app.after_request
    def common_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        response.headers.setdefault("Access-Control-Allow-Origin", "*")
        response.headers.setdefault("Access-Control-Allow-Headers", "Authorization, Content-Type, Accept, Idempotency-Key, If-Match, If-None-Match, X-HTTP-Method-Override, X-Client-Id")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        return response

    def negotiate():
        accept = request.headers.get("Accept", "application/json")
        accepted = [x.strip().split(";")[0].strip() for x in accept.split(",")]
        if "*/*" in accepted or "application/json" in accepted or "application/problem+json" in accepted:
            return
        fail(406, "Not acceptable", "This service only supports application/json responses.", "not-acceptable")

    def authenticate():
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {DEMO_TOKEN}":
            fail(401, "Unauthorized", "A valid Bearer token is required.", "unauthorized")

    def rate_limit():
        client = request.headers.get("X-Client-Id") or request.remote_addr or "unknown"
        now = time.monotonic()
        bucket = rate_state[client]
        while bucket and now - bucket[0] >= RATE_WINDOW:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT:
            retry = max(1, int(RATE_WINDOW - (now - bucket[0])))
            fail(429, "Too many requests", "The client has exceeded the rate limit.", "rate-limit", extra_headers={"Retry-After": str(retry)})
        bucket.append(now)
        request.rate_remaining = RATE_LIMIT - len(bucket)
        request.rate_limit = RATE_LIMIT

    @app.before_request
    def before():
        # OPTIONS is deliberately unauthenticated for CORS preflight/discovery.
        if request.method == "OPTIONS":
            return None
        negotiate()
        authenticate()
        rate_limit()
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and request.data:
            if request.mimetype != "application/json":
                fail(415, "Unsupported media type", "JSON request bodies are required.", "unsupported-media-type")

    @app.after_request
    def rate_headers(response):
        if hasattr(request, "rate_limit"):
            response.headers["X-RateLimit-Limit"] = str(request.rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(max(0, request.rate_remaining))
        return response

    def effective_method():
        if request.method == "POST":
            override = request.headers.get("X-HTTP-Method-Override", "").upper().strip()
            if override in {"PUT", "PATCH", "DELETE"}:
                return override
        return request.method

    def canonical_body(body):
        return json.dumps(body, sort_keys=True, separators=(",", ":"))

    def validate_create(body, key):
        if not isinstance(body, dict):
            fail(400, "Bad request", "Request body must be a JSON object.", "bad-request")
        if not key or not key.strip():
            fail(400, "Bad request", "Idempotency-Key header is required.", "bad-request")
        if not isinstance(body.get("studentId"), str) or not body["studentId"].strip():
            fail(400, "Bad request", "studentId is required.", "bad-request")
        if not isinstance(body.get("items"), list) or not body["items"]:
            fail(400, "Bad request", "items must be a non-empty array.", "bad-request")
        for i, item in enumerate(body["items"]):
            if not isinstance(item, dict):
                fail(400, "Bad request", f"items[{i}] must be an object.", "bad-request")
            if not isinstance(item.get("itemId"), str) or not item["itemId"].strip():
                fail(400, "Bad request", f"items[{i}].itemId is required.", "bad-request")
            q = item.get("quantity")
            if not isinstance(q, int) or isinstance(q, bool) or q <= 0:
                fail(400, "Bad request", f"items[{i}].quantity must be a positive integer.", "bad-request")
            try:
                price = Decimal(str(item.get("unitPrice")))
            except (InvalidOperation, ValueError, TypeError):
                fail(400, "Bad request", f"items[{i}].unitPrice must be numeric.", "bad-request")
            if price < 0:
                fail(400, "Bad request", f"items[{i}].unitPrice cannot be negative.", "bad-request")
        if not isinstance(body.get("paymentMethod"), str) or not body["paymentMethod"].strip():
            fail(400, "Bad request", "paymentMethod is required.", "bad-request")

    def etag(order):
        raw = json.dumps(order.public(), sort_keys=True, separators=(",", ":")).encode()
        return '"' + hashlib.sha256(raw).hexdigest()[:16] + '"'

    def get_order_or_404(order_id):
        order = store.find_by_id(order_id)
        if not order:
            fail(404, "Order not found", f"No order exists with id {order_id}.", "order-not-found")
        return order

    def order_response(order, status=200, location=None):
        headers = {"ETag": etag(order), "Cache-Control": "private, max-age=60"}
        if location:
            headers["Location"] = location
        return json_response(order.public(), status, headers)

    def maybe_304(order):
        current = etag(order)
        if request.headers.get("If-None-Match") == current:
            return make_response("", 304, {"ETag": current, "Cache-Control": "private, max-age=60"})
        return None

    @app.route("/orders", methods=["OPTIONS"])
    @app.route("/orders/<int:order_id>", methods=["OPTIONS"])
    @app.route("/orders/<int:order_id>/cancellation", methods=["OPTIONS"])
    def options(order_id=None):
        if request.path == "/orders":
            allow = "GET, POST, OPTIONS"
        elif request.path.endswith("/cancellation"):
            allow = "POST, OPTIONS"
        else:
            allow = "GET, PUT, OPTIONS"
        return make_response("", 204, {"Allow": allow, "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": allow, "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Idempotency-Key, If-Match, If-None-Match, X-HTTP-Method-Override, X-Client-Id"})

    @app.route("/orders", methods=["POST"])
    def create_order():
        if effective_method() != "POST":
            return update_order()
        body = request.get_json(silent=True)
        key = request.headers.get("Idempotency-Key")
        validate_create(body, key)
        fingerprint = hashlib.sha256(canonical_body(body).encode()).hexdigest()
        old = store.find_by_idempotency(key)
        if old:
            if old.request_fingerprint != fingerprint:
                fail(409, "Idempotency key conflict", "The same Idempotency-Key was used with a different request.", "idempotency-conflict")
            return order_response(old, 201, f"/orders/{old.order_id}")

        items = [OrderItem(x["itemId"], x["quantity"], Decimal(str(x["unitPrice"]))) for x in body["items"]]
        total = sum((x.line_total for x in items), Decimal("0.00"))
        if total <= 0:
            fail(422, "Order refused", "Order total must be greater than zero.", "order-refused")
        order_id = store.next_id()
        try:
            payment.charge(order_id, float(total), body["paymentMethod"], key)
        except PaymentRejected as exc:
            fail(422, "Payment declined", str(exc), "payment-declined")
        except PaymentUnavailable as exc:
            fail(503, "Payment service unavailable", str(exc), "payment-unavailable")
        order = Order(str(uuid.uuid4()), order_id, body["studentId"], items, body["paymentMethod"], total, "PENDING", 15, key, fingerprint, datetime.now(timezone.utc).isoformat())
        store.save(order)
        return order_response(order, 201, f"/orders/{order_id}")

    @app.route("/orders", methods=["GET"])
    def list_orders():
        student = request.args.get("studentId")
        status = request.args.get("status")
        if status and status.upper() not in {"PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"}:
            fail(400, "Bad request", "Unknown order status.", "bad-request")
        orders = store.find_all(student, status.upper() if status else None)
        return json_response([o.public() for o in orders])

    @app.route("/orders/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        order = get_order_or_404(order_id)
        cached = maybe_304(order)
        return cached if cached else order_response(order)

    @app.route("/orders/<int:order_id>", methods=["PUT"])
    def update_order(order_id):
        order = get_order_or_404(order_id)
        current = etag(order)
        if request.headers.get("If-Match") != current:
            fail(412, "Precondition failed", "If-Match does not match the current order representation.", "precondition-failed")
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or body.get("status") not in {"PENDING", "CONFIRMED", "COMPLETED"}:
            fail(400, "Bad request", "status must be PENDING, CONFIRMED, or COMPLETED.", "bad-request")
        if order.status == "CANCELLED":
            fail(409, "Order state conflict", "A cancelled order cannot be updated.", "order-conflict")
        order.status = body["status"]
        store.save(order)
        return order_response(order)

    @app.route("/orders/<int:order_id>/cancellation", methods=["POST"])
    def cancel_order(order_id):
        order = get_order_or_404(order_id)
        if request.get_json(silent=True) is not None:
            fail(400, "Bad request", "Cancellation does not accept a request body.", "bad-request")
        if order.status in {"CANCELLED", "COMPLETED"}:
            fail(409, "Order state conflict", f"Order {order_id} cannot be cancelled from state {order.status}.", "order-conflict")
        order.status = "CANCELLED"
        store.save(order)
        return order_response(order)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

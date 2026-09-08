import os

import pytest

from app import app, store
import app as app_module


@pytest.fixture(autouse=True)
def reset_store(monkeypatch):
    store._orders.clear()
    store._idempotency.clear()
    store._next_id = 1

    class FakePaymentClient:
        def charge(self, order_id, amount, payment_method, idempotency_key):
            return {"status": "captured", "transactionId": f"TX-{order_id}"}

    monkeypatch.setattr(app_module, "payment_client", FakePaymentClient())
    app.config.update(TESTING=True)

    yield


def valid_body():
    return {
        "studentId": "STU-1001",
        "items": [
            {
                "itemId": "ITEM-101",
                "quantity": 2,
                "unitPrice": 120.00,
            }
        ],
        "paymentMethod": "CARD",
    }


def test_create_order_returns_201_and_location_header():
    client = app.test_client()

    response = client.post(
        "/orders",
        json=valid_body(),
        headers={"Idempotency-Key": "key-001"},
    )

    assert response.status_code == 201
    assert response.headers["Location"] == "/orders/1"
    assert response.json["orderId"] == 1


def test_idempotent_repeat_returns_original_result():
    client = app.test_client()

    first = client.post(
        "/orders",
        json=valid_body(),
        headers={"Idempotency-Key": "key-002"},
    )
    second = client.post(
        "/orders",
        json=valid_body(),
        headers={"Idempotency-Key": "key-002"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json == first.json
    assert len(store._orders) == 1


def test_malformed_body_returns_400_problem_shape():
    client = app.test_client()

    response = client.post(
        "/orders",
        json={
            "studentId": "STU-1001",
            "items": [],
            "paymentMethod": "CARD",
        },
        headers={"Idempotency-Key": "key-003"},
    )

    assert response.status_code == 400
    assert response.content_type.startswith("application/problem+json")
    assert set(response.json) == {"type", "title", "status", "detail"}


def test_unknown_order_returns_404_problem():
    client = app.test_client()

    response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.content_type.startswith("application/problem+json")
    assert response.json["status"] == 404

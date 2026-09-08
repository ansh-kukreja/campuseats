# CampusEats Assignment 4 — Order Service

This implementation is based on the team's Assignment 2/3 Order Service boundary:

- Students place orders.
- Orders own order records and order status.
- `placeOrder(studentId, items, paymentMethod)` becomes `POST /orders`.
- `getOrder(orderId)` becomes `GET /orders/{orderId}`.
- `cancelOrder(orderId)` becomes `POST /orders/{orderId}/cancellation`.

## Project structure

```text
Assignment4_OrderService/
├── openapi.yaml
├── app.py
├── models.py
├── store.py
├── errors.py
├── payment_client.py
├── requirements.txt
├── NOTES.md
├── README.md
└── tests/
    └── test_orders.py
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export PAYMENTS_URL="http://localhost:8081/<Tutorial-4-payment-endpoint>"
python app.py
```

## Validate and test

```bash
openapi-spec-validator openapi.yaml
pytest -q
```

The service uses an in-process dictionary as permitted by Assignment 4. The outbound payment call is a real HTTP request using `requests`, with a timeout, exponential backoff, jitter, no retry on 4xx, and an `Idempotency-Key` on every payment attempt.

## Important

Do not submit a made-up payment endpoint. Replace `PAYMENTS_URL` with the endpoint exposed by your Tutorial 4 Payments service.

# CampusEats Assignment 4 — Order Service

## Team

- Gauraansh Gaur — 20251651039
- Shraiyansh Chaware — 20251651085
- Utkarsh Singh — 20251651099
- Abhishek Yadav — 20251651007
- Jatin Mandwani — 20251651048

## A4 resource table

| Method | URL | What it does | Success | Failure |
|---|---|---|---|---|
| POST | `/orders` | Creates an order and charges the selected payment method | 201 + Location | 400, 409, 422, 503 |
| GET | `/orders/{orderId}` | Reads one order | 200 | 404 |
| GET | `/orders?studentId=STU-1001` | Lists orders filtered by student; optional status filter | 200 | 400 |
| POST | `/orders/{orderId}/cancellation` | Changes an existing order to CANCELLED | 200 | 404, 409, 422 |

## A5 — hard resource decision

`placeOrder(studentId, items, paymentMethod)` was the least comfortable operation to map because the SOAP name describes a business action rather than a durable noun. I mapped it to `POST /orders` because the operation creates the durable `Order` owned by the Order Service. I rejected `/placeOrder` because the assignment requires verbs such as `place` or `get` to disappear from URLs. I also kept cancellation as the sub-resource `/orders/{orderId}/cancellation` because cancellation represents a state-changing operation attached to one existing order.

## D3 — fallback

The Order Service fails the create request with `503 Service Unavailable` if the Payments dependency remains unreachable after the configured safe retries. Degrading by creating an order without successful payment would violate the Assignment 3 business rule that payment is completed before the order is accepted, and it could create an unpaid order that appears valid.

## 1. WSDL versus OpenAPI line count

Fill this exact line-count comparison after opening the final Assignment 3 WSDL in the same editor used for the count:

- Assignment 3 WSDL lines: **TODO — count from partner.wsdl**
- Assignment 4 `openapi.yaml` lines: **TODO — run `wc -l openapi.yaml`**
- Difference: **TODO**

The difference is mainly structural: the WSDL contains SOAP/XML machinery such as messages, port types, bindings and SOAP-specific service/address declarations. The REST contract describes HTTP paths, methods, parameters, request/response bodies and reusable schemas instead.

Two things the WSDL declared that the OpenAPI file does not need in the same SOAP form are:
1. SOAP messages / message parts.
2. A WSDL `binding`/`port` describing SOAP transport and operation binding.

## 2. SOAP fault to REST problem

Assignment 3's UniPay fault was:

```xml
<soap:Fault>
  <faultcode>soap:Client</faultcode>
  <faultstring>Card declined</faultstring>
  <detail>
    <uni:error code="card_declined"/>
  </detail>
</soap:Fault>
```

The REST Order Service maps a payment rejection to:

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/problem+json

{
  "type": "https://campuseats.example.com/problems/payment-declined",
  "title": "Payment declined",
  "status": 422,
  "detail": "Payments service rejected the charge."
}
```

Returning an application error inside `200 OK` is a problem because intermediaries such as clients, proxies, gateways and monitoring systems interpret the HTTP status as successful transport/application completion. A failure encoded only inside a successful response body can therefore be cached, logged or handled as success. HTTP status codes let the network layer recognize the failure without understanding the application payload.

## 3. UDDI publish, find, bind

The three UDDI moves are reduced in the REST setup. The contract is still published so consumers can learn the API, and a client still needs to discover the service endpoint before making requests. The live UDDI-style registry/bind process disappears from the request path; the HTTP URL plus the OpenAPI contract take over the practical job of describing and reaching the service.

## 4. XML Schema validation versus REST code validation

The function carrying the responsibility that XML Schema previously handled is:

```text
validate()
```

in `app.py`.

It checks the request before the code accesses its fields. Without it, a request such as:

```json
{
  "studentId": "STU-1001",
  "items": [
    {"itemId": "ITEM-101", "quantity": -2, "unitPrice": 120}
  ],
  "paymentMethod": "CARD"
}
```

could reach the order logic with an invalid negative quantity.

## 5. Where SOAP would still be preferable

The Payments/UniPay boundary is the strongest case for keeping SOAP. The Assignment 3 integration already establishes that the bank controls a rigid WSDL and uses SOAP/WS-* guarantees for the payment edge. The guarantee being bought is a fixed, strongly described message/fault contract plus message-level security and the transactional/all-or-nothing behaviour expected by the bank. CampusEats should therefore keep SOAP at that partner boundary while using REST for its own resource-oriented services.

## Important configuration

Set `PAYMENTS_URL` to the **actual Tutorial 4 Payments endpoint** before running the Order Service.

Example:

```bash
export PAYMENTS_URL="http://localhost:8081/<your-tutorial-4-payment-endpoint>"
```

Do not replace this with a hard-coded URL in `payment_client.py`.

## Validation commands

```bash
python -m pip install -r requirements.txt
openapi-spec-validator openapi.yaml
pytest -q
```

The OpenAPI validator should finish without an error. `pytest` should report four passing tests.

## Curl evidence to capture

Run the Order Service and the Tutorial 4 Payments service, then capture these with `-i`:

1. Successful create:
```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-001" \
  -d '{"studentId":"STU-1001","items":[{"itemId":"ITEM-101","quantity":2,"unitPrice":120.00}],"paymentMethod":"CARD"}'
```

2. Same request and same key again:
```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-001" \
  -d '{"studentId":"STU-1001","items":[{"itemId":"ITEM-101","quantity":2,"unitPrice":120.00}],"paymentMethod":"CARD"}'
```

3. Malformed body:
```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-bad" \
  -d '{"studentId":"STU-1001","items":[],"paymentMethod":"CARD"}'
```

4. Missing resource:
```bash
curl -i http://127.0.0.1:5000/orders/999
```

5. State conflict:
```bash
curl -i -X POST http://127.0.0.1:5000/orders/1/cancellation
curl -i -X POST http://127.0.0.1:5000/orders/1/cancellation
```

The second cancellation should demonstrate the `409` state conflict.

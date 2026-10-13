# CampusEats Order Service - Assignment 6
## Team 06

- Gauraansh Gaur - 20251651039
- Shraiyansh Chaware - 20251651085
- Utkarsh Singh - 20251651099
- Abhishek Yadav - 20251651007
- Jatin Mandwani - 20251651048

# *A1 - HTTP status map*

## 1. Create an order - POST /orders

- 201 Created: The order was created successfully. The Location header identifies the new order.
- 400 Bad Request: The request body is malformed or cannot be parsed as valid JSON.
- 401 Unauthorized: The request does not contain a valid Bearer token.
- 406 Not Acceptable: The client requests an unsupported response format.
- 409 Conflict: The same idempotency key is reused with a different request.
- 415 Unsupported Media Type: The middleware rejects a non-JSON body when request is non-empty.
- 422 Unprocessable Entity: The order fails validation or a business rule, or the payment is declined.
- 429 Too Many Requests: The client exceeds the rate limit.
- 503 Service Unavailable: The payment service is unavailable after the permitted retries.

## 2. List orders - GET /orders

- 200 OK: The matching orders are returned, optionally filtered by student ID or status.
- 400 Bad Request: An invalid order status or query parameter is supplied.
- 401 Unauthorized: The request does not contain a valid Bearer token.
- 406 Not Acceptable: The client requests an unsupported response format.
- 429 Too Many Requests: The client exceeds the rate limit.

## 3. Retrieve an order - GET /orders/{orderId}

- 200 OK: The requested order is returned successfully.
- 304 Not Modified: The order has not changed since the version identified by the client's If-None-Match header.
- 401 Unauthorized: The request does not contain a valid Bearer token.
- 404 Not Found: The requested order does not exist.
- 406 Not Acceptable: The client requests an unsupported response format.
- 429 Too Many Requests: The client exceeds the rate limit.

## 4. Update an order - PUT /orders/{orderId}

- 200 OK: The order status is updated successfully.
- 400 Bad Request: The request body or requested status is invalid.
- 401 Unauthorized: The request does not contain a valid Bearer token.
- 404 Not Found: The requested order does not exist.
- 406 Not Acceptable: The client requests an unsupported response format.
- 409 Conflict: The order is in a state that prevents the requested update.
- 412 Precondition Failed: The supplied If-Match ETag does not match the current order representation.
- 415 Unsupported Media Type: A non-JSON body is sent.
- 429 Too Many Requests: The client exceeds the rate limit.

## 5. Cancel an order - POST /orders/{orderId}/cancellation

- 200 OK: The order is cancelled successfully.
- 400 Bad Request: The cancellation request contains an unsupported body.
- 401 Unauthorized: The request does not contain a valid Bearer token.
- 404 Not Found: The requested order does not exist.
- 406 Not Acceptable: The client requests an unsupported response format.
- 409 Conflict: The order is already cancelled or completed and cannot be cancelled again.
- 415 Unsupported Media Type: A non-JSON body is sent.
- 429 Too Many Requests: The client exceeds the rate limit.

# *A2 - Audit of HTTP 200 Responses*

Inspected the response helpers and route handlers in app.py for failure responses incorrectly returning 200 OK.
The order_response() helper defaults to 200, which is appropriate for successful retrieval, update, and cancellation 
operations. Order creation explicitly returns 201 Created. The inspected failure paths raise ProblemError with 
appropriate non-200 status codes rather than returning a failure body with 200 OK. No explicit failure-as-200 response 
was identified in the inspected code.

# *A3 - POST /orders 201 Created and Location Header*

Tested the order creation endpoint using curl with a JSON request body stored in `body.json`.

The server returned 201 Created, confirming that the order was successfully created. The response included the header 
Location: `/orders/1`, identifying the URI of the newly created order. The response body was JSON containing `orderId: 1`, 
status: PENDING, total: 100.0, and estimatedReadyMinutes: 15.

Therefore, the A3 requirement is satisfied.

# *A4 - Retry-After and Safe Retries*

Tested rate limiting by configuring `RATE_LIMIT=2` and sending repeated requests. The server returned `429 Too Many Requests` with a `Retry-After` header indicating how many seconds to wait before retrying.

Tested payment-service unavailability by configuring `PAYMENTS_URL` to point to an unavailable local endpoint. The server returned `503 Service Unavailable`, `Content-Type: application/problem+json`, and `Retry-After: 5`. The response contained Problem Details fields including `type`, `title`, `status`, and `detail`.

**Retry policy:** Clients should wait for the duration specified by Retry-After before retrying transient 429 or 503 responses. GET requests are safe to retry because they retrieve data without intentionally changing order state. POST /orders should be retried with the same Idempotency-Key and the same request body to prevent duplicate orders. State-changing requests, such as PUT and cancellation, should not be blindly retried when the outcome of the first attempt is uncertain. Other unchanged client errors (4xx responses, except transient rate limiting) should not be retried automatically.

# *B1 - Consistent Problem Details Error Responses*

Implemented consistent API error responses using the existing `problem()` helper in `errors.py`.

The application handles custom `ProblemError` exceptions and registered HTTP errors, including 404 Not Found, 405 Method Not Allowed, and 415 Unsupported Media Type. A general exception handler logs unexpected exceptions on the server and returns a generic 500 Internal Server Error response without exposing internal exception details to the client.

## Tests performed

1. Requested a nonexistent route with a valid Bearer token. The server returned `404 NOT FOUND` with `Content-Type: application/problem+json`.
2. Temporarily added a test route that raised a `RuntimeError`. The server returned `500 INTERNAL SERVER ERROR` with `Content-Type: application/problem+json` and a generic error message.
3. Confirmed that the responses contained the Problem Details fields `type`, `title`, `status`, and `detail`.

The temporary test route was used only for testing and was removed afterward.

## Result
The tested 404 and unexpected 500 error paths return consistent Problem Details JSON responses.

# *B2 - Stable Problem Type Catalogue*

The service uses stable Problem Details type URIs to identify categories of errors. The type URI is generated by the `problem()` helper using the error's `kind`.

| Stable type          | Meaning                                          |     HTTP status | Trigger                                                                                           |
|----------------------|--------------------------------------------------|----------------:|---------------------------------------------------------------------------------------------------|
| `empty-cart`         | The order contains no items.                     |             422 | The submitted items array is empty or missing.                                                    |
| `item-unavailable`   | An ordered item is unavailable.                  | Not implemented | Documented in the catalogue, but the current service has no menu or availability check.           |
| `payment-declined`   | The payment provider rejects the payment.        |             422 | `PaymentRejected` is raised.                                                                      |
| `order-not-found`    | The requested order does not exist.              |             404 | The order lookup returns no matching order.                                                       |
| `illegal-transition` | The requested order state change is not allowed. |             409 | An attempt is made to update a cancelled order or cancel an already cancelled or completed order. |

The corresponding type URIs follow this pattern:

`https://campuseats.example.com/problems/{type}`

For example, `order-not-found` produces `https://campuseats.example.com/problems/order-not-found`.

The `item-unavailable` type is documented but is not currently triggered by the implementation because no item availability data or checking logic exists.

# *B3 - Field-Level Validation Errors*

The CampusEats API returns field-level validation errors using the `errors` array in the Problem Details response. Each error contains a `field` identifying the invalid field and a `message` explaining the validation failure.

When multiple fields are invalid, the API collects all validation errors and returns them together in a single `422 Unprocessable Entity` response instead of stopping at the first invalid field.

The response uses the `application/problem+json` content type and includes the standard Problem Details fields: `type`, `title`, `status`, and `detail`.

**Example response:**

```json
{
  "type": "https://campuseats.example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields contain invalid values.",
  "errors": [
    {
      "field": "address",
      "message": "address is required."
    },
    {
      "field": "items[0].quantity",
      "message": "Quantity must be a positive integer."
    }
  ]
}
```

**Validation tests performed:**

1. Empty `studentId` and invalid quantity (`0`) returned `422` with both fields in `errors[]`.
2. Missing `address` returned `422` with an `address` validation error.
3. Missing `address` and invalid quantity returned `422` with both errors in the same response.
4. An empty `items` array returned `422`, with an `items` validation error and the stable `empty-cart` problem type.

## Result
B3 validation behavior was tested successfully. The API reports field-level errors in a consistent Problem Details response.

# *B4 - Unexpected Error Handling*

- Unexpected server-side exceptions are caught by a general exception handler.
- Exception details and tracebacks are logged on the server using `app.logger.exception()`.
- Clients receive a generic `500 Internal Server Error` response using the Problem Details format.
- Internal exception messages, tracebacks, and database details are not exposed to clients.
- Verified using a temporary test route that deliberately raised a `RuntimeError`. The response returned HTTP 500 with `Content-Type: application/problem+json`, while the traceback appeared in the Flask server terminal.
- The temporary test route was removed after testing.

# *C1 - POST /orders Request Validation*

- The POST /orders endpoint validates the request body before creating an order.
- The request body must be a JSON object.
- studentId must be a nonempty string.
- address is required and must be a nonempty string.
- items must be a nonempty list.
- Each item must be an object with a nonempty itemId.
- Each item's quantity must be a positive integer greater than or equal to 1. Boolean values are rejected.
- Each item's unitPrice must be a valid, finite, nonnegative number.
- Invalid request data returns HTTP 422 Unprocessable Entity with validation details in the errors[] array.
- An empty or missing items list uses the empty-cart problem type.

## Verification performed

1. Empty items list - returned 422.
2. quantity = 0 - returned 422.
3. Missing address - returned 422

# *C2 - Collect All Validation Errors*

- The `POST /orders` endpoint collects all request validation errors in an `errors[]` array.
- The API returns one `422 Unprocessable Entity` response containing all detected validation errors.
- Validation is performed before idempotency processing, payment charging, or order creation.
- If validation fails, execution stops before `payment.charge()` and `store.save()`.
- Verified using a request containing an empty `studentId`, an empty `address`, a zero quantity, and a missing `paymentMethod`. The API returned one `422` response containing all four errors.

# *C3 - Content Negotiation*

- Successful responses support JSON by default and XML when requested.
- Requests specifying an unsupported response format receive 406 Not Acceptable.
- Error responses use Problem Details JSON with Content-Type: application/problem+json.

## Verification performed
1. `Accept: application/json` - returned `200 OK` with JSON.
2. `Accept: application/xml` - returned `200 OK` with XML.
3. `Accept: text/csv` - returned `406 Not Acceptable`.

# *C4 - Content-Type Headers*

- Successful JSON responses use `Content-Type: application/json; charset=utf-8`.
- Successful XML responses use `Content-Type: application/xml; charset=utf-8`.
- Error responses use `Content-Type: application/problem+json; charset=utf-8`.
- The common response handler adds security and CORS headers.
- Responses without a body, such as `204 No Content` and `304 Not Modified`, do not require a `Content-Type` header.

## Verification performed
1. `GET /orders` with `Accept: application/json` - returned `200 OK` with the correct JSON content type and UTF-8 charset.
2. `GET /orders/999999` - returned `404 Not Found` with the correct Problem Details content type and UTF-8 charset.

# *D1 - Happy-path curl transcript*

The successful order-creation request was tested using `curl.exe -i`. The request included a valid JSON body with the required student ID, delivery address, items, quantities, unit prices, and payment method.

The service returned `201 CREATED`, indicating that the order was created successfully. The response included a `Location` header pointing to the newly created order and a JSON representation of the order.

## Observed response
- Status: `201 CREATED`
- Content-Type: `application/json; charset=utf-8`
- Location: `/orders/1`
- Response body:

```json
{
  "estimatedReadyMinutes": 15,
  "orderId": 1,
  "status": "PENDING",
  "total": 100.0
}
```

The complete request and response, including headers, are recorded in `curl-transcript.txt`.

# *D2 - Failure responses*
The following failure scenarios were tested to verify that the service returns meaningful HTTP status codes and consistent Problem Details responses.

| Scenario                                                         |            Expected status | Problem type or result                    |
|------------------------------------------------------------------|---------------------------:|-------------------------------------------|
| Empty cart                                                       | `422 Unprocessable Entity` | `empty-cart`                              |
| Quantity equal to zero                                           | `422 Unprocessable Entity` | Validation response containing `errors[]` |
| Unknown order ID                                                 |            `404 Not Found` | `order-not-found`                         |
| Repeated cancellation after the order has already been cancelled |             `409 Conflict` | `illegal-transition`                      |
| Rate limit exceeded                                              |    `429 Too Many Requests` | Problem Details with `Retry-After`        |

Validation failures identify the invalid field and explain the validation rule that was violated. Other failures use the common Problem Details structure containing `type`, `title`, `status`, and `detail`, with the content type `application/problem+json`.

The complete runtime status codes, headers, and response bodies should be retained in `curl-transcript.txt`.

# *D3 - Content negotiation*

The service was tested with an `Accept: application/xml` request header.

## Observed response
- Status: `200 OK`
- Content-Type: `application/xml; charset=utf-8`
- Response body:

```xml
<response></response>
```

The request demonstrated that the service selected an XML response when XML was requested. The response headers and body were captured from the running application.

The service returns JSON by default and uses `406 Not Acceptable` when the requested response representation is unsupported.

# *D4 - Regression checks*

Regression checks were performed to verify idempotency and payment-timeout handling.

## D4.1 - Idempotency: first request

A POST request to `/orders` was sent with the key `d4-idempotency-final-001` and the request body stored in `d4-idempotency.json`.

**Observed result:**
- Status: `201 CREATED`
- Location: `/orders/1`
- ETag: `"65fc46221db11734"`
- Order ID: `1`
- Total: `50.0`

## D4.2 - Idempotency: repeated request

The exact same request body and idempotency key were sent again.

### Observed result
- Status: `201 CREATED`
- Location: `/orders/1`
- ETag: `"65fc46221db11734"`
- Order ID: `1`
- Total: `50.0`

The repeated request returned the same order representation and order ID instead of creating a second order. This verifies the idempotency replay behavior for the tested request.

## D4.3 - Simulated payment timeout

A payment timeout was simulated through the Flask test client by injecting a payment function that raises `PaymentUnavailable`. No real payment request was made.

### Observed result
- Status: `503 Service Unavailable`
- Content-Type: `application/problem+json; charset=utf-8`
- Retry-After: `5`
- Problem type: `payment-unavailable`
- Title: `Payment service unavailable`
- Detail: `Payment service timed out.`

The test passed, confirming that the application maps the simulated payment-service failure to HTTP 503, returns Problem Details, and includes the `Retry-After: 5` header.

This was a simulated application-level test, not a real network timeout against an external payment service.

### Automated regression tests

The command `python -m pytest -v` completed successfully, with all **11 tests passing**.


# Q1) Your status map: every endpoint, its success status, and the status for each failure — one line on why each.

## `POST /orders` - Create an order
- **201 Created:** The order was created successfully; `Location` identifies the new order.
- **400 Bad Request:** The request body is malformed or invalid JSON.
- **401 Unauthorized:** The Bearer token is missing or invalid.
- **406 Not Acceptable:** The requested response representation is unsupported.
- **409 Conflict:** The same idempotency key is reused with a different request body.
- **415 Unsupported Media Type:** The request uses an unsupported content type.
- **422 Unprocessable Entity:** Request validation fails, the cart is empty, or payment is declined.
- **429 Too Many Requests:** The client exceeds the rate limit; `Retry-After` tells it when to retry.
- **503 Service Unavailable:** The payment service is unavailable; `Retry-After` advises the client when to retry.

## `GET /orders` - List orders
- **200 OK:** Returns matching orders, optionally filtered by `studentId` or `status`.
- **400 Bad Request:** A query parameter, such as the order status, is invalid.
- **401 Unauthorized:** The Bearer token is missing or invalid.
- **406 Not Acceptable:** The requested response representation is unsupported.
- **429 Too Many Requests:** The client exceeds the rate limit; `Retry-After` provides retry guidance.
- **500 Internal Server Error:** An unexpected server-side exception occurs; internal details are hidden.

## `GET /orders/{orderId}` - Retrieve an order
- **200 OK:** Returns the requested order.
- **304 Not Modified:** The order has not changed according to the `If-None-Match` validator.
- **401 Unauthorized:** The Bearer token is missing or invalid.
- **404 Not Found:** No order exists with the requested ID.
- **406 Not Acceptable:** The requested response representation is unsupported.
- **429 Too Many Requests:** The client exceeds the rate limit.
- **500 Internal Server Error:** An unexpected server-side exception occurs.

## `PUT /orders/{orderId}` - Update order status
- **200 OK:** The order status was updated successfully.
- **400 Bad Request:** The request body or requested status is invalid.
- **401 Unauthorized:** The Bearer token is missing or invalid.
- **404 Not Found:** The requested order does not exist.
- **406 Not Acceptable:** The requested response representation is unsupported.
- **409 Conflict:** The requested state transition is not allowed.
- **412 Precondition Failed:** The supplied `If-Match` ETag does not match the current order version.
- **415 Unsupported Media Type:** The request uses an unsupported content type.
- **429 Too Many Requests:** The client exceeds the rate limit.
- **500 Internal Server Error:** An unexpected server-side exception occurs.

## `POST /orders/{orderId}/cancellation` - Cancel an order
- **200 OK:** The order was cancelled successfully.
- **400 Bad Request:** The cancellation request contains an invalid or unsupported body.
- **401 Unauthorized:** The Bearer token is missing or invalid.
- **404 Not Found:** The requested order does not exist.
- **406 Not Acceptable:** The requested response representation is unsupported.
- **409 Conflict:** The order is already cancelled or completed and cannot be cancelled again.
- **415 Unsupported Media Type:** The request uses an unsupported content type.
- **429 Too Many Requests:** The client exceeds the rate limit.
- **500 Internal Server Error:** An unexpected server-side exception occurs.

## `OPTIONS` endpoints
- **`OPTIONS /orders` - 204 No Content:** Returns the supported-method information.
- **`OPTIONS /orders/{orderId}` - 204 No Content:** Returns the supported methods for an individual order.
- **`OPTIONS /orders/{orderId}/cancellation` - 204 No Content:** Returns the supported methods for cancellation.

The `OPTIONS` responses contain no response body. Unsupported methods are handled through the application's HTTP error handling.

# Q2) Your type catalogue: the stable string for each failure and what triggers it. 

The service represents Problem Details types as URIs following this pattern:

`https://campuseats.example.com/problems/{type}`

| Stable type | Trigger | HTTP status |
|---|---|---:|
| `empty-cart` | The submitted `items` array is empty or missing. | 422 |
| `item-unavailable` | An ordered item is unavailable. This type is documented but is not currently triggered because the application does not implement item-availability checking. | Not implemented |
| `payment-declined` | The payment provider rejects the payment and the application raises `PaymentRejected`. | 422 |
| `order-not-found` | The requested order ID does not match an existing order. | 404 |
| `illegal-transition` | An order-state transition is prohibited, such as cancelling an already cancelled or completed order. | 409 |

# Q3) Paste one Problem Details body from your service and label its fields.

The following is the recorded payment-timeout test result. The timeout was simulated using the Flask test client.

HTTP status: `503 Service Unavailable`

Content-Type: `application/problem+json; charset=utf-8`

Retry-After: `5`

```json
{
  "type": "https://campuseats.example.com/problems/payment-unavailable",
  "title": "Payment service unavailable",
  "status": 503,
  "detail": "Payment service timed out."
}
```

Field meanings:

- **`type`**: Stable URI identifying the category of failure.
- **`title`**: Short, human-readable summary of the problem.
- **`status`**: HTTP status code associated with the problem.
- **`detail`**: Safe explanation of this specific failure.
- **`Retry-After` header**: Tells the client to wait five seconds before retrying.

The `errors` array is optional and is included when field-level validation errors need to be reported.

# Q4. Show a field-level 422 that reports two bad fields at once. 

A `POST /orders` request with a missing address and an invalid quantity produces a `422 Unprocessable Entity` response containing both validation errors.

Content-Type: `application/problem+json; charset=utf-8`

```json
{
  "type": "https://campuseats.example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields contain invalid values.",
  "errors": [
    {
      "field": "address",
      "message": "address is required."
    },
    {
      "field": "items[0].quantity",
      "message": "Quantity must be a positive integer."
    }
  ]
}
```

- **`errors[0].field`** identifies the missing `address`.
- **`errors[0].message`** explains that an address is required.
- **`errors[1].field`** identifies the quantity of the first item.
- **`errors[1].message`** explains that quantity must be a positive integer.

The application collects validation errors before calling the payment adapter or saving the order. Therefore, multiple invalid fields can be reported in one response instead of stopping at the first validation failure.

# Q5) Which endpoints are safe to retry, and which status codes tell a client so? 

- **GET endpoints:** `GET /orders` and `GET /orders/{orderId}` are safe to retry because they retrieve data without intentionally changing order state.
- **OPTIONS endpoints:** These can generally be repeated because they discover supported methods and do not modify order state.
- **POST /orders:** This endpoint must not be blindly retried with a new idempotency key. A retry of the same operation must reuse the same `Idempotency-Key` and identical request body. The tested replay returned the original order rather than creating a duplicate.
- **PUT /orders/{orderId}:** Use `If-Match` to protect against stale updates. A `412 Precondition Failed` response indicates that the client must retrieve the current representation before attempting an update with a fresh ETag.
- **POST /orders/{orderId}/cancellation:** Do not blindly retry when the outcome is uncertain; first check the order's current state.

Retry signals:

- **429 Too Many Requests:** Wait for the duration indicated by `Retry-After`.
- **503 Service Unavailable:** Wait for the duration indicated by `Retry-After` before retrying the transient failure.
- **Other 4xx responses:** Do not automatically repeat an unchanged request. Correct the request, authentication, or precondition first.

A retry should only be attempted when the operation's semantics and idempotency behavior make it safe.

# Q6. Where did you map an internal error to a clean client error, and what did you hide from the caller? 

The order-creation implementation catches expected payment exceptions and maps them to controlled API responses:

- `PaymentRejected` is mapped to `422 Unprocessable Entity` with the stable type `payment-declined`.
- `PaymentUnavailable` is mapped to `503 Service Unavailable` with the stable type `payment-unavailable` and a `Retry-After` header.
- Unexpected server-side exceptions are logged using the server logger and returned to the client as a generic `500 Internal Server Error` Problem Details response.

The application does not expose raw exception messages, stack traces, credentials, provider response bodies, or internal network/database details to the caller. The detailed exception information remains in server-side logs for debugging.

Validation is performed before payment processing and order storage, so invalid requests do not proceed to those side effects.

# Q7. (If done) Show the same order as JSON and as XML, and the Accept header that chose each. 

The service uses the `Accept` header to select the response representation:

- `Accept: application/json` requests JSON.
- `Accept: application/xml` requests XML.
- `Accept: text/csv` requests an unsupported representation and results in `406 Not Acceptable`.

The recorded XML test returned:

HTTP status: `200 OK`

Content-Type: `application/xml; charset=utf-8`

```xml
<response></response>
```

**Evidence limitation:** This captured XML response represents an empty result. The current transcript does not establish that the same populated order was returned in both JSON and XML, so it would be inaccurate to claim that this requirement has been fully demonstrated.

To complete this item, create or identify an order, request a representation containing that order with `Accept: application/json`, and repeat the equivalent request with `Accept: application/xml`. Record both response bodies and headers in `curl-transcript.txt`, and paste the two observed representations here.













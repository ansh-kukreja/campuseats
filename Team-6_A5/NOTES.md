# CampusEats Order Service — Assignment 5 Notes
Team ID : 06
Name : Gauraansh Gaur
Roll no : 20251651039

Name : Shraiyansh Chaware
Roll no : 20251651085

Name : Abhishek Yadav
Roll no : 20251651007

Name : Utkarsh Singh
Roll no : 20251651099

Name : Jatin Mandwani
Roll no : 20251651048

## 1. HTTP method, status-code and header mapping
- POST /orders → 201 Created; uses Authorization, Accept, Idempotency-Key; returns Location, ETag and Cache-Control.
- GET /orders → 200 OK; supports studentId/status filters.
- GET /orders/{orderId} → 200 OK; returns ETag and Cache-Control.
- PUT /orders/{orderId} → 200 OK; uses If-Match and returns a new ETag.
- POST /orders/{orderId}/cancellation → cancellation operation.
- OPTIONS → 204 No Content and Allow header.
- Common errors use application/problem+json.

## 2. Safe and idempotent methods
GET and OPTIONS are safe. GET is idempotent. PUT is idempotent when the same update is repeated. POST is not generally idempotent, so order creation uses Idempotency-Key.

## 3. Conditional GET
The service returns an ETag. A client sends it using If-None-Match. If unchanged, the server returns 304 Not Modified instead of the complete representation.

## 4. Conditional write
PUT uses If-Match. If the supplied ETag does not match the current resource version, the server returns 412 Precondition Failed.

## 5. 400 vs 422
400 is for malformed/invalid request syntax or required request data. 422 is for a syntactically valid request that cannot be accepted as a domain operation, such as a rejected payment.

## 6. CORS
The service sends CORS response headers and supports OPTIONS preflight requests.

## 7. Cache-Control
Cache-Control describes how the representation can be cached. Together with ETag and If-None-Match it supports conditional GET.

## 8. Why GET for search/listing
Listing orders is retrieval, so GET is used. studentId and status are query parameters.

## 9. Location with 201
After creating an order, 201 Created is returned with a Location header identifying the new resource. A Location header does not require a 3xx response.

## 10. OPTIONS and Allow
OPTIONS describes supported operations. Allow lists the methods supported by the resource.

## 11. Method override
The service includes support for X-HTTP-Method-Override for clients that need to tunnel an HTTP method through POST.

## 12. Content negotiation
The Accept header is checked. Unsupported media types result in 406 Not Acceptable.

## 13. Authorization
Protected endpoints require a Bearer Authorization header. Missing/invalid credentials result in 401 Unauthorized.

## 14. Rate limiting
Responses expose X-RateLimit-Limit and X-RateLimit-Remaining. Exceeding the per-client limit returns 429 Too Many Requests with Retry-After.

## 15. Security headers
Responses include X-Content-Type-Options: nosniff and Strict-Transport-Security.

## 16. Idempotency
Create requests use Idempotency-Key. Repeating the same request with the same key does not create another order. Reusing a key for a materially different request is treated as a conflict.

## 17. Payment
The payment adapter supports Razorpay credentials through RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET. Demo mode is available for assignment tests when real credentials are not configured. Secrets should never be committed.

## 18. Validation evidence
The project includes pytest tests and an OpenAPI specification. The final terminal evidence should be produced with:
python -m pytest -q
python -m openapi_spec_validator openapi.yaml


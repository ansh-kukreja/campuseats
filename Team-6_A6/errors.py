from flask import jsonify

PROBLEM_TYPES = {
    "empty-cart": "The order contains no items.",
    "item-unavailable": "An ordered item is unavailable.",
    "payment-declined": "The payment was declined.",
    "order-not-found": "The requested order does not exist.",
    "illegal-transition": "The requested order state transition is not allowed.",
}


class ProblemError(Exception):
    def __init__(self, status, title, detail, kind="bad-request", extra_headers=None, errors=None):
        self.status = status
        self.title = title
        self.detail = detail
        self.kind = kind
        self.extra_headers = extra_headers or {}
        self.errors = errors or []
        super().__init__(detail)


def problem(status, title, detail, kind="bad-request", extra_headers=None, errors=None):
    body = {
        "type": f"https://campuseats.example.com/problems/{kind}",
        "title": title,
        "status": status,
        "detail": detail
    }

    if errors:
        body["errors"] = errors

    response = jsonify(body)
    response.status_code = status
    response.headers["Content-Type"] = "application/problem+json; charset=utf-8"
    for k, v in (extra_headers or {}).items(): response.headers[k] = v
    return response

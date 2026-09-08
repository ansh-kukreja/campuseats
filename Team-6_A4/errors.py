from __future__ import annotations

from dataclasses import dataclass
from flask import jsonify


@dataclass
class ProblemError(Exception):
    status: int
    title: str
    detail: str
    type_name: str

    def __str__(self) -> str:
        return self.detail


def problem(
    status: int,
    title: str,
    detail: str,
    type_name: str,
):
    """The one error-shape helper required by Assignment 4."""
    body = {
        "type": f"https://campuseats.example.com/problems/{type_name}",
        "title": title,
        "status": status,
        "detail": detail,
    }
    response = jsonify(body)
    response.status_code = status
    response.content_type = "application/problem+json"
    return response


def register_error_handlers(app) -> None:
    @app.errorhandler(ProblemError)
    def handle_problem_error(exc: ProblemError):
        return problem(exc.status, exc.title, exc.detail, exc.type_name)

    @app.errorhandler(400)
    def handle_bad_request(_exc):
        return problem(
            400,
            "Bad request",
            "The request body or parameters are malformed.",
            "bad-request",
        )

    @app.errorhandler(404)
    def handle_framework_not_found(_exc):
        return problem(
            404,
            "Resource not found",
            "The requested resource does not exist.",
            "not-found",
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(_exc):
        return problem(
            400,
            "Bad request",
            "The HTTP method is not supported for this resource.",
            "bad-request",
        )

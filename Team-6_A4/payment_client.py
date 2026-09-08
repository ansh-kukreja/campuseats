from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from typing import Any

import requests


class PaymentRejected(Exception):
    pass


class PaymentUnavailable(Exception):
    pass


@dataclass
class PaymentClient:
    """
    Outbound Payments client.

    PAYMENTS_URL is the complete endpoint and must be supplied through an
    environment variable. No CampusEats service URL is hard-coded here.
    """

    base_url: str | None = None
    timeout_seconds: float = 3.0
    max_attempts: int = 3
    initial_backoff_seconds: float = 0.20

    def __post_init__(self) -> None:
        self.base_url = self.base_url or os.getenv("PAYMENTS_URL")
        if not self.base_url:
            raise RuntimeError(
                "PAYMENTS_URL must point to the Tutorial 4 Payments endpoint."
            )

    def charge(
        self,
        order_id: int,
        amount: float,
        payment_method: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        payload = {
            "amount": amount,
            "paymentMethod": payment_method,
            "orderRef": f"CE-ORD-{order_id}",
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Idempotency-Key": idempotency_key,
        }

        for attempt in range(1, self.max_attempts + 1):
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout_seconds,
                )

                # Never retry a 4xx: the request was rejected and repeating it
                # cannot repair a client/domain error.
                if 400 <= response.status_code < 500:
                    raise PaymentRejected(
                        f"Payments service rejected the charge with HTTP "
                        f"{response.status_code}."
                    )

                # Retry transient 5xx responses.
                if 500 <= response.status_code < 600:
                    if attempt == self.max_attempts:
                        raise PaymentUnavailable(
                            "Payments service returned a 5xx response after "
                            f"{self.max_attempts} attempts."
                        )
                    self._sleep_with_backoff_and_jitter(attempt)
                    continue

                if not 200 <= response.status_code < 300:
                    raise PaymentUnavailable(
                        f"Unexpected Payments response: HTTP {response.status_code}."
                    )

                try:
                    return response.json()
                except ValueError:
                    return {"status": "approved"}

            except requests.RequestException as exc:
                if attempt == self.max_attempts:
                    raise PaymentUnavailable(
                        f"Payments service unreachable after {self.max_attempts} attempts."
                    ) from exc
                self._sleep_with_backoff_and_jitter(attempt)

        raise PaymentUnavailable("Payments service unavailable.")

    def _sleep_with_backoff_and_jitter(self, attempt: int) -> None:
        exponential = self.initial_backoff_seconds * (2 ** (attempt - 1))
        jitter = random.uniform(0, 0.10)
        time.sleep(exponential + jitter)

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass
class OrderItem:
    item_id: str
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Order:
    # Internal record fields. These are not all published.
    internal_id: str
    order_id: int
    student_id: str
    items: list[OrderItem]
    payment_method: str
    total: Decimal
    status: str
    estimated_ready_minutes: int
    idempotency_key: str
    request_fingerprint: str
    _created_at: str = field(default="")

    def as_json(self) -> dict[str, Any]:
        """Public representation; internal identifiers and retry metadata never leak."""
        return {
            "orderId": self.order_id,
            "status": self.status,
            "total": float(self.total),
            "estimatedReadyMinutes": self.estimated_ready_minutes,
        }

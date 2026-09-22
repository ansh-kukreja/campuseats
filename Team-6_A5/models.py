from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrderItem:
    item_id: str
    quantity: int
    unit_price: Decimal
    @property
    def line_total(self):
        return self.unit_price * self.quantity

@dataclass
class Order:
    internal_id: str
    order_id: int
    student_id: str
    items: list
    payment_method: str
    total: Decimal
    status: str
    estimated_ready_minutes: int
    idempotency_key: str
    request_fingerprint: str
    created_at: str
    version: int = 1

    def public(self):
        return {"orderId": self.order_id, "status": self.status, "total": float(self.total), "estimatedReadyMinutes": self.estimated_ready_minutes}

from __future__ import annotations

from typing import Optional

from models import Order


class OrderStore:
    """In-process storage for the Assignment 4 service."""

    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._idempotency: dict[str, int] = {}
        self._next_id = 1

    def next_id(self) -> int:
        order_id = self._next_id
        self._next_id += 1
        return order_id

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order
        self._idempotency[order.idempotency_key] = order.order_id

    def find_by_id(self, order_id: int) -> Optional[Order]:
        return self._orders.get(order_id)

    def find_by_idempotency_key(self, key: str) -> Optional[Order]:
        order_id = self._idempotency.get(key)
        if order_id is None:
            return None
        return self.find_by_id(order_id)

    def find_all(
        self,
        student_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[Order]:
        orders = list(self._orders.values())
        if student_id is not None:
            orders = [o for o in orders if o.student_id == student_id]
        if status is not None:
            orders = [o for o in orders if o.status == status]
        return sorted(orders, key=lambda o: o.order_id)

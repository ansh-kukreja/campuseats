class OrderStore:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}
        self.next_order_id = 1
    def next_id(self):
        x = self.next_order_id; self.next_order_id += 1; return x
    def save(self, order):
        self.orders[order.order_id] = order
        self.idempotency[order.idempotency_key] = order.order_id
    def find_by_id(self, order_id): return self.orders.get(order_id)
    def find_by_idempotency(self, key):
        oid = self.idempotency.get(key)
        return self.orders.get(oid) if oid else None
    def find_all(self, student_id=None, status=None):
        values = list(self.orders.values())
        if student_id: values = [x for x in values if x.student_id == student_id]
        if status: values = [x for x in values if x.status == status]
        return sorted(values, key=lambda x: x.order_id)

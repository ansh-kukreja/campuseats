import os
import requests

class PaymentRejected(Exception): pass
class PaymentUnavailable(Exception): pass

class PaymentClient:
    """Razorpay-compatible payment adapter. Tests inject a charge function.
    Production use requires RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET."""
    def __init__(self, charge=None): self._charge = charge
    def charge(self, order_id, amount, payment_method, idempotency_key):
        if self._charge: return self._charge(order_id, amount, payment_method, idempotency_key)
        key_id=os.getenv("RAZORPAY_KEY_ID"); key_secret=os.getenv("RAZORPAY_KEY_SECRET")
        if not key_id or not key_secret:
            # Assignment/test mode: no real charge is attempted when credentials are absent.
            return {"id": f"demo_pay_{order_id}", "status":"created"}
        try:
            r=requests.post("https://api.razorpay.com/v1/orders", auth=(key_id,key_secret), json={"amount":int(round(amount*100)),"currency":"INR","receipt":f"CE-ORD-{order_id}","notes":{"paymentMethod":payment_method}}, headers={"Idempotency-Key":idempotency_key}, timeout=5)
        except requests.RequestException as exc:
            raise PaymentUnavailable("Razorpay is unavailable.") from exc
        if 400 <= r.status_code < 500: raise PaymentRejected(f"Razorpay rejected the payment request (HTTP {r.status_code}).")
        if r.status_code >= 500: raise PaymentUnavailable(f"Razorpay returned HTTP {r.status_code}.")
        if not 200 <= r.status_code < 300: raise PaymentUnavailable(f"Unexpected Razorpay response: HTTP {r.status_code}.")
        return r.json()

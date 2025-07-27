import httpx
from typing import Optional
from app.domain.ports.order_status_notifier_port import OrderStatusNotifierPort

class OrderStatusNotifierHttp(OrderStatusNotifierPort):
    def __init__(self, base_url: str, client: Optional[httpx.Client] = None):
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=5)

    def notify(self, order_id: int, status: str) -> None:
        payload = {"order_id": order_id, "status": status}
        resp = self.client.post(f"{self.base_url}/api/order/payment-status", json=payload)
        resp.raise_for_status()  # levanta exceção se 4xx/5xx

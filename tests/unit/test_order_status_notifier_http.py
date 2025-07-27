import httpx
from app.adapters.driven.notifiers.order_status_notifier_http import OrderStatusNotifierHttp

def test_http_notifier_sends_correct_payload():
    expected = {"order_id": 42, "status": "PAID"}
    called = {}

    # ----- Fake client ---------------------------------
    class FakeClient:
        def post(self, url, *, json):
            called["url"] = url
            called["json"] = json
            class Resp:
                status_code = 200
                def raise_for_status(self):  # noqa: D401
                    pass
            return Resp()

    notifier = OrderStatusNotifierHttp(
        "http://order-service:8000", FakeClient()  # ⬅️ injeta o fake
    )

    # ----- Act -----------------------------------------
    notifier.notify(42, "PAID")

    # ----- Assert --------------------------------------
    assert called["url"] == "http://order-service:8000/api/order/payment-status"
    assert called["json"] == expected

from pytest_bdd import scenarios, given, when, then
from fastapi.testclient import TestClient
from app.shared.enums.payment_status import PaymentStatus

scenarios("features/confirm_payment.feature")


@given("existe um pagamento pendente para o pedido 20")
def create_payment(client: TestClient):
    client.post("/api/payment", json={"order_id": 20, "amount": 30})


@when("o provedor envia um webhook de pagamento PAID para o pedido 20")
def send_webhook(client: TestClient):
    client.post(
        "/api/payment/webhook",
        json={"order_id": 20, "payment_status": PaymentStatus.PAID.value},
    )


@then("o status do pagamento do pedido 20 é PAID")
def check_paid(client: TestClient):
    r = client.get("/api/payment/20")
    assert r.json()["status"] == "PAID"

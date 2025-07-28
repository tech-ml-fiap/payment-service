from app.shared.enums.payment_status import PaymentStatus

def test_create_and_get(client):
    body = {"order_id": 10, "amount": 50.0}
    r = client.post("/api/payment", json=body)
    assert r.status_code == 201
    qr = r.json()["qr_data"]

    r = client.get("/api/payment/10")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "PENDING"
    assert data["qr_code"] == qr



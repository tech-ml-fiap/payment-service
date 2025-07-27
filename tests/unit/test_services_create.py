from app.domain.services.create_payment_service import CreatePaymentService
from app.shared.enums.payment_status import PaymentStatus


def fake_qr(order_id, amount):
    return f"QR-{order_id}-{amount}"


def test_create_payment(repo):
    service = CreatePaymentService(repo, fake_qr)
    qr = service.execute(order_id=1, amount=25.5)

    assert qr == "QR-1-25.5"
    p = repo.get_by_order_id(1)
    assert p.status is PaymentStatus.PENDING
    assert p.qr_code == qr

from datetime import datetime
from app.domain.services.update_payment_status_service import UpdatePaymentStatusService
from app.domain.entities.payment import Payment
from app.shared.enums.payment_status import PaymentStatus


def test_update_paid(repo):
    # cria pagamento pendente
    repo.create(Payment(id=None, order_id=1, amount=10.0))
    service = UpdatePaymentStatusService(repo)

    updated = service.execute(1, PaymentStatus.PAID, "ok")

    assert updated.status is PaymentStatus.PAID
    assert updated.description == "ok"
    assert isinstance(updated.payment_date, datetime)


def test_update_not_found(repo):
    service = UpdatePaymentStatusService(repo)
    import pytest
    with pytest.raises(ValueError):
        service.execute(99, PaymentStatus.PAID)

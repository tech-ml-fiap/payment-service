from datetime import datetime
from typing import List

import pytest

from app.domain.entities.payment import Payment
from app.domain.services.update_payment_status_service import (
    UpdatePaymentStatusService,
)
from app.shared.enums.payment_status import PaymentStatus
from app.domain.ports.order_status_notifier_port import OrderStatusNotifierPort


# -----------------------
# Fake / Spy Notifier
# -----------------------
class FakeNotifier(OrderStatusNotifierPort):
    def __init__(self) -> None:
        self.calls: List[tuple[int, str]] = []

    def notify(self, order_id: int, status: str) -> None:  # noqa: D401
        self.calls.append((order_id, status))


# -----------------------
# Happy Path
# -----------------------
def test_update_paid(repo):
    # 1) cria pagamento pendente
    repo.create(Payment(id=None, order_id=1, amount=10.0))

    spy = FakeNotifier()
    service = UpdatePaymentStatusService(repo, spy)

    updated = service.execute(1, PaymentStatus.PAID, "ok")

    # domínio alterado
    assert updated.status is PaymentStatus.PAID
    assert updated.description == "ok"
    assert isinstance(updated.payment_date, datetime)

    # notificação disparada
    assert spy.calls == [(1, "PAID")]


# -----------------------
# Not-found Path
# -----------------------
def test_update_not_found(repo):
    spy = FakeNotifier()
    service = UpdatePaymentStatusService(repo, spy)

    with pytest.raises(ValueError):
        service.execute(99, PaymentStatus.PAID, "nada")

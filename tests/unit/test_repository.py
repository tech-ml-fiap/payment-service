from app.domain.entities.payment import Payment
from app.shared.enums.payment_status import PaymentStatus


def test_crud(repo):
    p = Payment(id=None, order_id=2, amount=30.0)
    created = repo.create(p)
    assert created.id is not None

    fetched = repo.get_by_order_id(2)
    assert fetched.id == created.id

    fetched.status = PaymentStatus.CANCELED
    repo.update(fetched)
    assert repo.get_by_order_id(2).status is PaymentStatus.CANCELED

    assert repo.list_pending() == []  # sem pendentes agora

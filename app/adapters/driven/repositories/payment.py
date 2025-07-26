from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.payment import Payment
from app.domain.ports.payment_repository_port import PaymentRepositoryPort
from app.adapters.driven.models.payment_model import PaymentModel


class PaymentRepository(PaymentRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    # helpers
    @staticmethod
    def _to_domain(model: PaymentModel) -> Payment:
        return Payment(
            id=model.id, order_id=model.order_id, amount=model.amount,
            qr_code=model.qr_code, status=model.status,
            payment_date=model.payment_date, description=model.description
        )

    # CRUD
    def create(self, payment: Payment) -> Payment:
        m = PaymentModel(**payment.__dict__)
        self.session.add(m); self.session.commit(); self.session.refresh(m)
        return self._to_domain(m)

    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        m = (self.session.query(PaymentModel)
                       .filter_by(order_id=order_id).first())
        return self._to_domain(m) if m else None

    def list_pending(self) -> List[Payment]:
        return [self._to_domain(m)
                for m in self.session.query(PaymentModel)
                                     .filter_by(status="PENDING").all()]

    def update(self, payment: Payment) -> Payment:
        m: PaymentModel = (self.session.query(PaymentModel)
                                      .filter_by(id=payment.id).first())
        if not m:
            raise ValueError("Payment not found")

        for field in payment.__dict__:
            setattr(m, field, getattr(payment, field))
        self.session.commit(); self.session.refresh(m)
        return self._to_domain(m)

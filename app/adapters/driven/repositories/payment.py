from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.payment import Payment
from app.adapters.driven.models.payment_model import PaymentModel
from app.shared.enums.payment_status import PaymentStatus


class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    # ---------- helpers ----------
    @staticmethod
    def _to_domain(m: PaymentModel) -> Payment:
        return Payment(
            id=m.id,
            order_id=m.order_id,
            amount=m.amount,
            qr_code=m.qr_code,
            status=m.status,
            payment_date=m.payment_date,
            description=m.description,
        )

    # ---------- C ----------
    def create(self, payment: Payment) -> Payment:
        model = PaymentModel(
            order_id=payment.order_id,
            amount=payment.amount,
            qr_code=payment.qr_code,
            status=payment.status,
            payment_date=payment.payment_date,
            description=payment.description,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_domain(model)

    # ---------- R ----------
    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        m = self.session.query(PaymentModel).filter_by(order_id=order_id).first()
        return self._to_domain(m) if m else None

    def list_pending(self) -> List[Payment]:
        return [
            self._to_domain(m)
            for m in self.session.query(PaymentModel)
            .filter_by(status=PaymentStatus.PENDING)
            .all()
        ]

    # ---------- U ----------
    def update(self, payment: Payment) -> Payment:
        model: PaymentModel = self.session.query(PaymentModel).get(payment.id)
        if not model:
            raise ValueError("Payment not found")

        model.order_id = payment.order_id
        model.amount = payment.amount
        model.qr_code = payment.qr_code
        model.status = payment.status
        model.payment_date = payment.payment_date
        model.description = payment.description

        self.session.commit()
        self.session.refresh(model)
        return self._to_domain(model)

from sqlalchemy import Column, Integer, Float, String, Enum, DateTime
from app.shared.enums.payment_status import PaymentStatus
from app.shared.mixins.timestamp_mixin import TimestampMixin
from database import Base


class PaymentModel(TimestampMixin, Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True, nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    qr_code = Column(String, nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    payment_date = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Payment(order={self.order_id}, status={self.status})>"

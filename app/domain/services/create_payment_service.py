from app.domain.entities.payment import Payment
from app.domain.ports.payment_repository_port import PaymentRepositoryPort
from app.shared.enums.payment_status import PaymentStatus
from typing import Callable


class CreatePaymentService:
    def __init__(self, repo: PaymentRepositoryPort, qr_generator: Callable):
        self.repo = repo
        self.qr_generator = qr_generator

    def execute(self, order_id: int, amount: float) -> str:
        self._validate_amount(amount)
        self._validate_not_exists(order_id)

        qr_data = self.qr_generator(order_id, amount)
        payment = Payment(
            id=None,
            order_id=order_id,
            amount=amount,
            qr_code=qr_data,
            status=PaymentStatus.PENDING,
            description="Aguardando pagamento",
        )
        self.repo.create(payment)
        return qr_data

    def _validate_amount(self, amount: float):
        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero")

    def _validate_not_exists(self, order_id: int):
        if self.repo.get_by_order_id(order_id):
            raise ValueError("Pagamento já existe para este pedido.")

from datetime import datetime
from typing import Optional
from app.core.ports.payment_repository_port import PaymentRepositoryPort
from app.shared.enums.payment_status import PaymentStatus
from app.core.entities.payment import Payment

class UpdatePaymentStatusService:
    def __init__(self, payment_repository: PaymentRepositoryPort):
        self.payment_repository = payment_repository

    def execute(self, order_id: int, new_status: PaymentStatus, description: Optional[str] = None) -> Payment:
        """
        Atualiza o status do pagamento associado ao pedido.
        Se o status for PAID, atualiza a data de pagamento para o momento atual.
        """
        payment = self.payment_repository.get_by_order_id(order_id)
        if not payment:
            raise ValueError("Pagamento não encontrado para o pedido.")

        payment.status = new_status
        payment.description = description
        if new_status == PaymentStatus.PAID:
            payment.payment_date = datetime.now()

        updated_payment = self.payment_repository.update(payment)
        return updated_payment

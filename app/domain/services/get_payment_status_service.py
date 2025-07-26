from app.core.entities.payment import Payment
from app.core.ports.payment_repository_port import PaymentRepositoryPort

class GetPaymentStatusService:
    def __init__(self, payment_repository: PaymentRepositoryPort):
        self.payment_repository = payment_repository

    def execute(self, order_id: int) -> Payment:
        """
        Retorna o status de pagamento do pedido.
        Levanta ValueError se nenhum pagamento for encontrado.
        """
        payment = self.payment_repository.get_by_order_id(order_id)
        if not payment:
            raise ValueError("Pagamento não encontrado para o pedido.")
        return payment

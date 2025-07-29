from typing import List

from app.adapters.driven.repositories.payment import PaymentRepository
from app.domain.entities.payment import Payment


class ListPaymentsService:
    """
    Serviço de listagem paginada de pagamentos.

    Argumentos:
        payment_repo (PaymentRepository): repositório de pagamentos.
    """

    def __init__(self, payment_repo: PaymentRepository) -> None:
        self._payment_repo = payment_repo

    def execute(self, skip: int = 0, limit: int = 50) -> List[Payment]:
        """
        Retorna uma lista de objetos Payment.

        Args:
            skip (int): quantidade de registros a pular (offset). Deve ser >= 0.
            limit (int): quantidade máxima de registros retornados. Deve ser > 0.

        Raises:
            ValueError: se skip < 0 ou limit <= 0.

        Returns:
            List[Payment]: lista de pagamentos.
        """
        if skip < 0:
            raise ValueError("skip deve ser >= 0")
        if limit <= 0:
            raise ValueError("limit deve ser > 0")

        return self._payment_repo.list_all(skip=skip, limit=limit)

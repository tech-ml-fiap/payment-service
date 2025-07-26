from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Optional
from app.domain.entities.payment import Payment


class PaymentRepositoryPort(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment: ...
    @abstractmethod
    def get_by_order_id(self, order_id: int) -> Optional[Payment]: ...
    @abstractmethod
    def list_pending(self) -> Iterable[Payment]: ...
    @abstractmethod
    def update(self, payment: Payment) -> Payment: ...

from abc import ABC, abstractmethod

class OrderStatusNotifierPort(ABC):
    @abstractmethod
    def notify(self, order_id: int, status: str) -> None:
        """Envia o novo status do pedido para o order-service."""

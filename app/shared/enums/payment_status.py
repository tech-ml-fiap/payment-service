from enum import Enum

class PaymentStatus(Enum):
    PENDING = "Pendente"
    PAID = "Pago"
    FAILED = "Falha"
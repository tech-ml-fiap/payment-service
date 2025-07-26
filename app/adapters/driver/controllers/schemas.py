from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.shared.enums.payment_status import PaymentStatus


class PaymentCreateIn(BaseModel):      # recebido do Order Service
    order_id: int
    amount  : float

class PaymentQRCodeOut(BaseModel):
    qr_data: str

class PaymentStatusOut(BaseModel):
    order_id: int
    status  : PaymentStatus
    qr_code : Optional[str] = None
    amount  : float
    payment_date: Optional[datetime]
    description : Optional[str]

class WebhookIn(BaseModel):
    order_id: int
    payment_status: PaymentStatus
    description: Optional[str] = None

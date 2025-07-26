from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Payment:
    id:          Optional[int]
    order_id:    int
    amount:      float
    qr_code:     Optional[str] = None
    status:      PaymentStatus = PaymentStatus.PENDING
    payment_date:Optional[datetime] = None
    description: Optional[str] = None

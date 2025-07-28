from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.adapters.driver.controllers.schemas import (
    PaymentCreateIn,
    PaymentQRCodeOut,
    WebhookIn,
    PaymentStatusOut,
)
from app.domain.services import (
    create_payment_service as cps,
    get_payment_status_service as gps,
    update_payment_status_service as ups,
)
from app.adapters.driven.repositories.payment import PaymentRepository
from app.shared.enums.payment_status import PaymentStatus
from app.shared.generate_qr_data import generate_qr_data
from app.adapters.driver.dependencies import get_db

router = APIRouter()


@router.post("", response_model=PaymentQRCodeOut, status_code=201)
def create_payment(body: PaymentCreateIn, db: Session = Depends(get_db)):
    try:
        repo = PaymentRepository(db)
        service = cps.CreatePaymentService(repo, generate_qr_data)
        qr = service.execute(order_id=body.order_id, amount=body.amount)
        return PaymentQRCodeOut(qr_data=qr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=PaymentStatusOut)
def get_status(order_id: int, db: Session = Depends(get_db)):
    repo = PaymentRepository(db)
    service = gps.GetPaymentStatusService(repo)
    try:
        p = service.execute(order_id)
        return PaymentStatusOut(
            order_id=p.order_id,
            status=p.status,
            qr_code=p.qr_code,
            amount=p.amount,
            payment_date=p.payment_date,
            description=p.description,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(404, str(e))


@router.post("/webhook", status_code=200)
def webhook(body: WebhookIn, db: Session = Depends(get_db)):
    repo = PaymentRepository(db)
    service = ups.UpdatePaymentStatusService(repo)
    # try:
    #     status_enum = PaymentStatus(body.payment_status)
    # except ValueError:
    #     raise HTTPException(400, "payment_status inválido")
    try:
        p = service.execute(body.order_id, body.payment_status, body.description)
        return PaymentStatusOut(
            order_id=p.order_id,
            status=p.status,
            qr_code=p.qr_code,
            amount=p.amount,
            payment_date=p.payment_date,
            description=p.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(404, str(e))

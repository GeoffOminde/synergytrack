from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Payment, Campaign

router = APIRouter()

@router.post("/mpesa")
async def mpesa_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    # Simplified parse; adjust to actual callback structure
    ref = data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")
    result_code = data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
    pay = db.query(Payment).filter(Payment.external_ref == ref).first()
    if pay:
        if result_code == 0 or result_code == "0":
            pay.status = "success"
            c = db.get(Campaign, pay.campaign_id)
            c.amount_raised += pay.amount
        else:
            pay.status = "failed"
        db.commit()
    return {"ok": True}

@router.post("/paystack")
async def paystack_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    event = data.get("event")
    ref = data.get("data", {}).get("reference")
    pay = db.query(Payment).filter(Payment.external_ref == ref).first()
    if pay and event == "charge.success":
        pay.status = "success"
        c = db.get(Campaign, pay.campaign_id)
        c.amount_raised += pay.amount
        db.commit()
    return {"ok": True}

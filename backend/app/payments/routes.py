from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Payment, Campaign
from ..security import current_user
from .mpesa import stk_push
from .paystack import initialize

router = APIRouter()

@router.post("/mpesa/stk")
def mpesa_stk(campaign_id: int, phone: str, amount: int, db: Session = Depends(get_db), user=Depends(current_user)):
    c = db.get(Campaign, campaign_id)
    if not c or c.status != "active": raise HTTPException(400, "Invalid campaign")
    ref = f"CMP{campaign_id}-U{user.id}"
    p = Payment(campaign_id=campaign_id, user_id=user.id, provider="mpesa", amount=amount, currency=c.currency, status="pending", external_ref=ref)
    db.add(p); db.commit()
    res = stk_push(phone, amount, ref, f"Donation to campaign {campaign_id}")
    return {"request": res, "reference": ref}

@router.post("/paystack/init")
def paystack_init(campaign_id: int, email: str, amount: int, db: Session = Depends(get_db), user=Depends(current_user)):
    c = db.get(Campaign, campaign_id)
    if not c or c.status != "active": raise HTTPException(400, "Invalid campaign")
    ref = f"CMP{campaign_id}-U{user.id}"
    p = Payment(campaign_id=campaign_id, user_id=user.id, provider="paystack", amount=amount, currency=c.currency, status="pending", external_ref=ref)
    db.add(p); db.commit()
    init = initialize(amount * 100, email, ref, callback_url="https://your-frontend/callback/paystack")
    return {"auth_url": init["data"]["authorization_url"], "reference": ref}

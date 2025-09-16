from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Campaign
from ..schemas import CampaignCreate, CampaignOut

router = APIRouter()

@router.post("/", response_model=CampaignOut)
def create_campaign(body: CampaignCreate, db: Session = Depends(get_db)):
    c = Campaign(project_id=body.project_id, goal_amount=body.goal_amount, currency=body.currency)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/", response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@router.get("/{id}", response_model=CampaignOut)
def get_campaign(id: int, db: Session = Depends(get_db)):
    return db.get(Campaign, id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Project, KPIRecord
from ..schemas import ProjectCreate, ProjectOut, KPIRecordIn, KPIRecordOut
from ..security import current_user
from ..ai.keras_model import infer_kpi

router = APIRouter()

@router.post("/", response_model=ProjectOut)
def create_project(body: ProjectCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    p = Project(org_id=body.org_id, title=body.title, sdg_targets=",".join(body.sdg_targets), description=body.description)
    db.add(p); db.commit(); db.refresh(p)
    return ProjectOut(id=p.id, org_id=p.org_id, title=p.title, sdg_targets=p.sdg_targets.split(","), description=p.description)

@router.get("/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    rows = db.query(Project).all()
    return [ProjectOut(id=r.id, org_id=r.org_id, title=r.title, sdg_targets=r.sdg_targets.split(","), description=r.description) for r in rows]

@router.post("/{project_id}/kpi", response_model=KPIRecordOut)
def add_kpi(project_id: int, body: KPIRecordIn, db: Session = Depends(get_db), user=Depends(current_user)):
    # Inference expects last 12 periods; for MVP we infer just on this metrics snapshot
    metrics_vec = list(body.metrics.values())
    ai = infer_kpi(metrics_vec)
    rec = KPIRecord(project_id=project_id, period=body.period, metrics=body.metrics, ai_flags={"anomaly": ai["anomaly"]}, forecast={"yhat": ai["forecast"]})
    db.add(rec); db.commit(); db.refresh(rec)
    return rec

@router.get("/{project_id}/kpi", response_model=list[KPIRecordOut])
def list_kpi(project_id: int, db: Session = Depends(get_db)):
    return db.query(KPIRecord).filter(KPIRecord.project_id == project_id).all()

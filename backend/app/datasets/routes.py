from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Dataset
from ..schemas import DatasetCreate
from ..security import current_user

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_dataset(meta: DatasetCreate = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(current_user)):
    content = await file.read()
    # Store locally for MVP; swap with S3/Azure in prod
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f: f.write(content)
    d = Dataset(org_id=meta.org_id, project_id=meta.project_id, title=meta.title, access_level=meta.access_level, storage_url=path)
    db.add(d); db.commit(); db.refresh(d)
    return {"id": d.id, "title": d.title, "url": d.storage_url}

@router.get("/", response_model=list[dict])
def list_datasets(db: Session = Depends(get_db)):
    return [{"id": d.id, "title": d.title, "access_level": d.access_level} for d in db.query(Dataset).all()]

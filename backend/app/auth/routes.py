from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..security import hash_password, create_tokens
from ..schemas import LoginIn, RegisterIn, UserOut

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(name=body.name, email=body.email, password_hash=hash_password(body.password), role="project_manager")
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not u.verify_password(body.password):
        raise HTTPException(401, "Invalid credentials")
    access, refresh = create_tokens(str(u.id))
    return {"access_token": access, "refresh_token": refresh, "user": {"id": u.id, "name": u.name, "role": u.role}}

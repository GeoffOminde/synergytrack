from datetime import datetime, timedelta, timezone
import jwt
from passlib.hash import argon2
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .models import User
from .db import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(pw: str) -> str:
    return argon2.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return argon2.verify(pw, hashed)

def create_token(sub: str, ttl_minutes: int):
    exp = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    return jwt.encode({"sub": sub, "exp": exp}, settings.SECRET_KEY, algorithm="HS256")

def create_tokens(sub: str):
    return (
        create_token(sub, settings.ACCESS_TTL_MIN),
        jwt.encode(
            {"sub": sub, "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TTL_DAYS)},
            settings.SECRET_KEY, algorithm="HS256"
        )
    )

def current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    db = SessionLocal()
    user = db.get(User, int(sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user

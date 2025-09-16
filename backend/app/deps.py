from fastapi import Depends, HTTPException
from .security import current_user

def require_role(*roles: str):
    def wrapper(user = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper

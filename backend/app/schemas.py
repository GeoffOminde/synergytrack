from pydantic import BaseModel, EmailStr
from typing import Optional, Any

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    org_id: Optional[int]
    class Config: from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class OrgCreate(BaseModel):
    name: str
    type: str
    country: str

class ProjectCreate(BaseModel):
    org_id: int
    title: str
    sdg_targets: list[str]
    description: str

class ProjectOut(BaseModel):
    id: int
    org_id: int
    title: str
    sdg_targets: list[str]
    description: str
    class Config: from_attributes = True

class KPIRecordIn(BaseModel):
    period: str
    metrics: dict[str, float]

class KPIRecordOut(BaseModel):
    id: int
    period: str
    metrics: dict
    ai_flags: dict | None
    forecast: dict | None
    class Config: from_attributes = True

class CampaignCreate(BaseModel):
    project_id: int
    goal_amount: int
    currency: str = "KES"

class CampaignOut(BaseModel):
    id: int
    project_id: int
    goal_amount: int
    currency: str
    amount_raised: int
    status: str
    class Config: from_attributes = True

class DatasetCreate(BaseModel):
    org_id: int
    project_id: int | None = None
    title: str
    access_level: str = "public"

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, JSON, Numeric, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .db import Base
from .security import verify_password

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="viewer")
    org_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def verify_password(self, pw: str) -> bool:
        return verify_password(pw, self.password_hash)

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(20))  # NGO/GOV/BIZ
    country: Mapped[str] = mapped_column(String(2))
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    title: Mapped[str] = mapped_column(String(200))
    sdg_targets: Mapped[str] = mapped_column(String(200))  # CSV list
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active")
    start_date: Mapped[datetime | None] = mapped_column(DateTime)
    end_date: Mapped[datetime | None] = mapped_column(DateTime)
    kpi_schema: Mapped[dict | None] = mapped_column(JSON)

class KPIRecord(Base):
    __tablename__ = "kpi_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    period: Mapped[str] = mapped_column(String(10))  # e.g. 2025-09
    metrics: Mapped[dict] = mapped_column(JSON)
    ai_flags: Mapped[dict | None] = mapped_column(JSON)
    forecast: Mapped[dict | None] = mapped_column(JSON)

class Campaign(Base):
    __tablename__ = "campaigns"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    goal_amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="KES")
    amount_raised: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="active")

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[str] = mapped_column(String(16))  # mpesa/paystack
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(16), default="pending")
    external_ref: Mapped[str | None] = mapped_column(String(64))
    receipt: Mapped[str | None] = mapped_column(String(64))
    metadata: Mapped[dict | None] = mapped_column(JSON)

class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String(200))
    schema: Mapped[dict | None] = mapped_column(JSON)
    license: Mapped[str] = mapped_column(String(100), default="CC-BY-4.0")
    access_level: Mapped[str] = mapped_column(String(16), default="public")  # public/restricted/private
    storage_url: Mapped[str] = mapped_column(String(512))
    checksum: Mapped[str | None] = mapped_column(String(64))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .auth.routes import router as auth_router
from .projects.routes import router as projects_router
from .datasets.routes import router as datasets_router
from .campaigns.routes import router as campaigns_router
from .payments.routes import router as payments_router
from .payments.webhooks import router as webhooks_router
from .ai.routes import router as ai_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SynergyTrack API",
    description="SynergyTrack — Partnerships, Crowdfunding, Data Sharing, and AI Monitoring for SDG17",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://your-domain"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(datasets_router, prefix="/datasets", tags=["datasets"])
app.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])
app.include_router(webhooks_router, prefix="/payments/webhooks", tags=["webhooks"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])

@app.get("/health")
def health():
    return {"ok": True}

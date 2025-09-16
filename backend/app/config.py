import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_NAME = "SynergyTrack"
    ENV = os.getenv("ENV", "dev")
    SECRET_KEY = os.getenv("JWT_SECRET", "change_me")
    ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "30"))
    REFRESH_TTL_DAYS = int(os.getenv("REFRESH_TTL_DAYS", "7"))

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sdg:sdg@db:5432/sdg17")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

    BLOB_BUCKET = os.getenv("BLOB_BUCKET", "")
    BLOB_REGION = os.getenv("BLOB_REGION", "")
    BLOB_ACCESS_KEY = os.getenv("BLOB_ACCESS_KEY", "")
    BLOB_SECRET_KEY = os.getenv("BLOB_SECRET_KEY", "")

    MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "")
    MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY", "")
    MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "")
    MPESA_BASE = os.getenv("MPESA_BASE", "https://sandbox.safaricom.co.ke")

    PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET", "")

    HF_OFFLINE = os.getenv("HF_OFFLINE", "false").lower() == "true"

settings = Settings()

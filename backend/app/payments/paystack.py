import requests
from ..config import settings

BASE = "https://api.paystack.co"

def initialize(amount_kobo: int, email: str, reference: str, callback_url: str):
    payload = {"amount": amount_kobo, "email": email, "reference": reference, "callback_url": callback_url}
    r = requests.post(f"{BASE}/transaction/initialize", json=payload, headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET}"})
    r.raise_for_status()
    return r.json()

def verify(reference: str):
    r = requests.get(f"{BASE}/transaction/verify/{reference}", headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET}"})
    r.raise_for_status()
    return r.json()

import base64, datetime, requests
from . import routes
from ..config import settings

def _timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def _password(ts: str):
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{ts}".encode()
    return base64.b64encode(raw).decode()

def _oauth_token():
    r = requests.get(
        f"{settings.MPESA_BASE}/oauth/v1/generate?grant_type=client_credentials",
        auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    )
    r.raise_for_status()
    return r.json()["access_token"]

def stk_push(phone: str, amount: int, reference: str, desc: str):
    ts = _timestamp()
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": _password(ts),
        "Timestamp": ts,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": reference,
        "TransactionDesc": desc
    }
    token = _oauth_token()
    r = requests.post(
        f"{settings.MPESA_BASE}/mpesa/stkpush/v1/processrequest",
        json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    r.raise_for_status()
    return r.json()

import base64
import hmac
import json
import time
from hashlib import sha256
from secrets import compare_digest, token_urlsafe

from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import Response

from app.config import settings

password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def _sign(payload: str) -> str:
    return hmac.new(settings.secret_key.encode(), payload.encode(), sha256).hexdigest()


def create_session_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "expires_at": int(time.time()) + settings.session_expire_hours * 3600,
        "nonce": token_urlsafe(16),
    }
    raw_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    return f"{raw_payload}.{_sign(raw_payload)}"


def read_session_token(token: str | None) -> int | None:
    if not token or "." not in token:
        return None
    raw_payload, signature = token.rsplit(".", 1)
    if not compare_digest(_sign(raw_payload), signature):
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(raw_payload.encode()).decode())
    except (ValueError, json.JSONDecodeError):
        return None
    if int(payload.get("expires_at", 0)) < int(time.time()):
        return None
    return int(payload["user_id"])


def set_session_cookie(response: Response, user_id: int) -> None:
    response.set_cookie(
        settings.session_cookie_name,
        create_session_token(user_id),
        httponly=True,
        samesite="lax",
        secure=settings.session_cookie_secure,
        max_age=settings.session_expire_hours * 3600,
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(settings.session_cookie_name)


def create_csrf_token(user_id: int) -> str:
    raw = f"{user_id}:{token_urlsafe(24)}"
    return f"{raw}.{_sign(raw)}"


def validate_csrf_token(token: str | None, user_id: int) -> bool:
    if not token or "." not in token:
        return False
    raw, signature = token.rsplit(".", 1)
    return raw.startswith(f"{user_id}:") and compare_digest(_sign(raw), signature)


def get_cookie_user_id(request: Request) -> int | None:
    return read_session_token(request.cookies.get(settings.session_cookie_name))

import hashlib
import secrets
import time

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Details API")

_PBKDF2_ROUNDS = 200_000
_TOKEN_TTL_SECONDS = 3600
_ADMIN_SALT = b"pythonwithchatgpt-admin-salt"
_USERS = {
    "admin": {
        "password_salt": _ADMIN_SALT.hex(),
        "password_hash": hashlib.pbkdf2_hmac(
            "sha256",
            b"admin123",
            _ADMIN_SALT,
            _PBKDF2_ROUNDS,
        ).hex(),
        "details": {"username": "admin", "email": "admin@example.com"},
    }
}
_TOKENS: dict[str, dict[str, str | float]] = {}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(payload: LoginRequest):
    user = _USERS.get(payload.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload_hash = hashlib.pbkdf2_hmac(
        "sha256",
        payload.password.encode(),
        bytes.fromhex(user["password_salt"]),
        _PBKDF2_ROUNDS,
    ).hex()
    if not secrets.compare_digest(user["password_hash"], payload_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(24)
    _TOKENS[token] = {"username": payload.username, "expires_at": time.time() + _TOKEN_TTL_SECONDS}
    return {"access_token": token, "token_type": "bearer"}


@app.get("/userdetails")
def userdetails(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = _TOKENS.get(token)
    if not session or session["expires_at"] < time.time():
        _TOKENS.pop(token, None)
        raise HTTPException(status_code=401, detail="Invalid token")

    return _USERS[session["username"]]["details"]

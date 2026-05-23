import hashlib
import os
import secrets
import time

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Details API")

_PBKDF2_ROUNDS = 200_000
_TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))


def _build_default_users():
    username = os.getenv("API_USERNAME", "admin")
    password = os.getenv("API_PASSWORD", "admin123")
    salt = os.urandom(16)
    return {
        username: {
            "password_salt": salt.hex(),
            "password_hash": hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt,
                _PBKDF2_ROUNDS,
            ).hex(),
            "details": {"username": username, "email": f"{username}@example.com"},
        }
    }


_USERS = _build_default_users()
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

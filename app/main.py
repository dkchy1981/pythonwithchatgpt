import hashlib
import secrets

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Details API")

_USERS = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "details": {"username": "admin", "email": "admin@example.com"},
    }
}
_TOKENS: dict[str, str] = {}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(payload: LoginRequest):
    user = _USERS.get(payload.username)
    payload_hash = hashlib.sha256(payload.password.encode()).hexdigest()
    if not user or user["password_hash"] != payload_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = secrets.token_urlsafe(24)
    _TOKENS[token] = payload.username
    return {"access_token": token, "token_type": "bearer"}


@app.get("/userdetails")
def userdetails(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    scheme, _, token = authorization.partition(" ")
    username = _TOKENS.get(token) if scheme.lower() == "bearer" else None
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    return _USERS[username]["details"]

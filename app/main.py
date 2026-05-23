from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Details API")

_USERS = {
    "admin": {
        "password": "admin123",
        "details": {"username": "admin", "email": "admin@example.com"},
    }
}
_TOKEN = "basic-token"


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(payload: LoginRequest):
    user = _USERS.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": _TOKEN, "token_type": "bearer"}


@app.get("/userdetails")
def userdetails(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != _TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    return _USERS["admin"]["details"]

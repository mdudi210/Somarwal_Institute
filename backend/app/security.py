from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .models import User

settings = get_settings()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 12 * 60


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_token(user: User, minutes: int | None = None, token_type: str = "access", jti: str | None = None) -> str:
    expires_delta = timedelta(minutes=minutes) if minutes is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "type": token_type,
        "jti": jti or str(uuid4()),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    csrf_token = secrets.token_urlsafe(32)
    response.set_cookie(
        key="somarwal_access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="somarwal_refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="somarwal_csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("somarwal_access_token", path="/")
    response.delete_cookie("somarwal_refresh_token", path="/")
    response.delete_cookie("somarwal_csrf_token", path="/")


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    token = request.cookies.get("somarwal_access_token")
    if not token:
        raise credentials_error

    if request.method not in ["GET", "HEAD", "OPTIONS"]:
        csrf_header = request.headers.get("x-csrf-token")
        csrf_cookie = request.cookies.get("somarwal_csrf_token")
        if not csrf_header or not csrf_cookie or csrf_header != csrf_cookie:
            raise HTTPException(status_code=403, detail="CSRF token validation failed")

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
        if payload.get("type") != "access":
            raise credentials_error
    except (JWTError, TypeError, ValueError):
        raise credentials_error
        
    user = db.get(User, user_id)
    if not user or not user.status:
        raise credentials_error
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in {"SUPER_ADMIN", "ADMIN", "STAFF"}:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

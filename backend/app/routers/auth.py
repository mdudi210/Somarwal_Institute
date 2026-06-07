from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from uuid import uuid4

from ..config import get_settings
from ..database import get_db
from ..models import User, Session as DBSession
from ..schemas import LoginRequest, UserCreate, VerifyOTPRequest
from ..security import (
    create_token, get_current_user, hash_password, verify_password,
    set_auth_cookies, clear_auth_cookies, settings, REFRESH_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role=payload.role.upper(),
        email_verified=True,
        phone_verified=True
    )
    db.add(user)
    db.commit()
    
    return {"status": True, "message": "Registration successful"}

@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user.last_login = datetime.utcnow()
    
    access_token = create_token(user, token_type="access")
    refresh_jti = str(uuid4())
    refresh_token = create_token(user, token_type="refresh", jti=refresh_jti)
    
    expires_at = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    db_session = DBSession(user_id=user.id, jti=refresh_jti, session_expires_at=expires_at)
    db.add(db_session)
    db.commit()
    
    set_auth_cookies(response, access_token, refresh_token)
    
    return {"status": True, "role": user.role, "name": user.name, "email": user.email, "phone": user.phone}


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    token = request.cookies.get("somarwal_refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = int(payload.get("sub"))
        jti = payload.get("jti")
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    db_session = db.query(DBSession).filter(DBSession.jti == jti, DBSession.user_id == user_id).first()
    if not db_session or db_session.is_revoked:
        clear_auth_cookies(response)
        raise HTTPException(status_code=401, detail="Session revoked or invalid")
        
    if datetime.utcnow() > db_session.session_expires_at:
        clear_auth_cookies(response)
        raise HTTPException(status_code=401, detail="Session expired")
        
    user = db.get(User, user_id)
    if not user or not user.status:
        raise HTTPException(status_code=401, detail="User inactive")
        
    new_jti = str(uuid4())
    db_session.is_revoked = True
    
    expires_at = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    new_session = DBSession(user_id=user.id, jti=new_jti, session_expires_at=expires_at)
    db.add(new_session)
    db.commit()
    
    access_token = create_token(user, token_type="access")
    refresh_token = create_token(user, token_type="refresh", jti=new_jti)
    
    set_auth_cookies(response, access_token, refresh_token)
    
    return {"status": True, "message": "Tokens refreshed"}


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    token = request.cookies.get("somarwal_refresh_token")
    if token:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            jti = payload.get("jti")
            db_session = db.query(DBSession).filter(DBSession.jti == jti).first()
            if db_session:
                db_session.is_revoked = True
                db.commit()
        except JWTError:
            pass
            
    clear_auth_cookies(response)
    return {"status": True, "message": "Logged out"}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role}

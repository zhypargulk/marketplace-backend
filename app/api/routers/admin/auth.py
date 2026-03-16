from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginRequest, Token


router = APIRouter(prefix="/v1/admin/auth", tags=["admin:auth"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, settings=Depends(get_settings)) -> Token:
    if data.email != settings.admin_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Admin password is stored in plain form in env; hash it on the fly for comparison
    if data.password != settings.admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(subject=settings.admin_email)
    return Token(access_token=access_token)


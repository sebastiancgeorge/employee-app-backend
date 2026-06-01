from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from auth import service as auth_service
from auth.schemas import LoginRequest, TokenResponse, RefreshTokenRequest
from database import get_db

router = APIRouter(prefix="/auth", tags = ["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends() , db: AsyncSession = Depends(get_db)):
    return await auth_service.login(db,form.username, form.password)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshTokenRequest):
    return await auth_service.refresh(body.refresh_token)
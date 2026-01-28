from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from schemas.auth import (TokenPairResponse,
                          LoginRequest,
                          AccessTokenResponse,
                          RefreshRequest,
                          LogoutRequest)
from schemas.user import UserCreate, UserRead
from db.session import get_db
from services.auth import AuthService

router = APIRouter(tags=["Auth"])
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)
):
    return await auth_service.register(user_data=user, db=db)

@router.post("/login", response_model=TokenPairResponse)
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    tokens =  await auth_service.login(db=db, email=data.email, password=data.password)

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 15,
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/auth/refresh",
    )

    return tokens



@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    new_access = await auth_service.refresh(
        db=db,
        refresh_token=refresh_token,
    )

    response.set_cookie(
        key="access_token",
        value=new_access["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 15,
        path="/",
    )

    return new_access


@router.post("/logout")
async def logout(data: LogoutRequest, db: AsyncSession = Depends(get_db)):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth/refresh")
    await auth_service.logout(db=db, refresh_token=data.refresh_token)
    return {"detail": "Logged out"}

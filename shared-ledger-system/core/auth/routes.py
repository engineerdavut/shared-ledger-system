# core/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.base import get_session
from core.auth import service, models, schemas
from typing import Any

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Any:
    user = await service.authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(
        data=schemas.TokenPayload(sub=user.username, user_id=user.id).model_dump()
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_create: schemas.UserCreate, session: AsyncSession = Depends(get_session)
) -> models.User:
    db_user = await service.get_user_by_username(session, username=user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await service.create_user(session, user_create)


@router.get("/me", response_model=schemas.UserSchema)
async def get_current_user_profile(
    current_user: models.User = Depends(service.get_current_user),
) -> models.User:
    return current_user

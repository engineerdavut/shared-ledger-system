# core/auth/schemas.py
from pydantic import BaseModel, EmailStr, field_serializer
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    user_id: int
    exp: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.isoformat()

    model_config = {"from_attributes": True}

from __future__ import annotations

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.user import UserStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    department: Optional[str] = None
    assigned_training: Optional[int] = None
    completed_training: Optional[int] = None
    status: Optional[UserStatus] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    assigned_training: Optional[int] = None
    completed_training: Optional[int] = None
    status: Optional[UserStatus] = None


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedUsers(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    per_page: int

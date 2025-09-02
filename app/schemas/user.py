from __future__ import annotations

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class PaginatedUsers(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    per_page: int

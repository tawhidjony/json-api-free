from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime
import enum

from app.db.base import Base


class UserStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    assigned_training: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    completed_training: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    status: Mapped[UserStatus | None] = mapped_column(
        SqlEnum(UserStatus), 
        nullable=True, 
        default=UserStatus.pending
    )  # pending, approved, rejected by admin
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

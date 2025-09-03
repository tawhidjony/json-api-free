from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, data: UserCreate) -> User:
    # Optional pre-check for friendlier error
    existing = db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(email=data.email, full_name=data.full_name, department=data.department, assigned_training=data.assigned_training, completed_training=data.completed_training, status=data.status)
    print(user)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Fallback in case of race condition
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def update_user(db: Session, user_id: int, data: UserUpdate) -> User | None:
    user = db.get(User, user_id)
    if not user:
        return None
    if data.email is not None:
        # Ensure email doesn't conflict
        other = db.execute(select(User).where(User.email == data.email, User.id != user_id)).scalar_one_or_none()
        if other:
            raise HTTPException(status_code=409, detail="Email already exists")
        user.email = data.email
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.department is not None:
        user.department = data.department
    if data.assigned_training is not None:
        user.assigned_training = data.assigned_training
    if data.completed_training is not None:
        user.completed_training = data.completed_training
    if data.status is not None:
        user.status = data.status
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def list_users(db: Session, page: int = 1, per_page: int = 10) -> tuple[list[User], int]:
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    total = db.scalar(select(func.count()).select_from(User))
    items = (
        db.execute(
            select(User).order_by(User.id).offset((page - 1) * per_page).limit(per_page)
        )
        .scalars()
        .all()
    )
    return items, int(total or 0)

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut, PaginatedUsers
from app.crud.user import create_user, get_user, update_user, delete_user, list_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=201)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, payload)


@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    ok = delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@router.get("/", response_model=PaginatedUsers)
def list_users_endpoint(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    items, total = list_users(db, page=page, per_page=per_page)
    return {"items": items, "total": total, "page": page, "per_page": per_page}

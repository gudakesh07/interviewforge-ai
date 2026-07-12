from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.security_service import get_cookie_user_id

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(request: Request, db: DbSession) -> User | None:
    user_id = get_cookie_user_id(request)
    if user_id is None:
        return None
    return db.get(User, user_id)


def require_user(request: Request, db: DbSession) -> User:
    user = get_current_user(request, db)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


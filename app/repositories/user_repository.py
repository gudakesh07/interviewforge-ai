from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User, UserSettings
from app.services.security_service import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def create_user(db: Session, username: str, email: str, password: str) -> User:
    user = User(username=username.strip(), email=email.lower().strip(), password_hash=hash_password(password))
    db.add(user)
    db.flush()
    db.add(UserSettings(user_id=user.id))
    db.commit()
    db.refresh(user)
    return user


from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import create_user, get_user_by_email, get_user_by_username
from app.services.security_service import clear_session_cookie, set_session_cookie, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request, "error": None})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(..., min_length=2, max_length=80),
    email: str = Form(..., min_length=5, max_length=255),
    password: str = Form(..., min_length=8, max_length=128),
    repeat_password: str = Form(..., min_length=8, max_length=128),
    db: Session = Depends(get_db),
):
    if password != repeat_password:
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": "Пароли не совпадают."}, status_code=400)
    if get_user_by_email(db, email) or get_user_by_username(db, username):
        return templates.TemplateResponse("auth/register.html", {"request": request, "error": "Email или username уже занят."}, status_code=400)
    user = create_user(db, username, email, password)
    response = RedirectResponse("/dashboard", status_code=303)
    set_session_cookie(response, user.id)
    return response


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": None})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(..., max_length=255),
    password: str = Form(..., max_length=128),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Неверный email или пароль."}, status_code=400)
    user.last_login_at = datetime.utcnow()
    db.commit()
    response = RedirectResponse("/dashboard", status_code=303)
    set_session_cookie(response, user.id)
    return response


@router.post("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    clear_session_cookie(response)
    return response


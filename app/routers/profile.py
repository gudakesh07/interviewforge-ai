from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
def profile(request: Request, user: User | None = Depends(get_current_user)):
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("profile/index.html", {"request": request, "user": user})


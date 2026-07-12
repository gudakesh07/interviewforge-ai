import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import create_database
from app.routers import api_interviews, auth, interviews, pages, profile, reports
from app.routers import settings as settings_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.app_debug)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(pages.router)
    app.include_router(auth.router)
    app.include_router(interviews.router)
    app.include_router(reports.router)
    app.include_router(profile.router)
    app.include_router(settings_router.router)
    app.include_router(api_interviews.router)

    @app.on_event("startup")
    def on_startup() -> None:
        logger.info("Starting InterviewForge AI")
        create_database()

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        return response

    @app.exception_handler(404)
    async def not_found(request: Request, exc):
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

    return app


app = create_app()


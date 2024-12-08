import os
import sys
from typing import Any

# Add the project root to the Python path
project_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# print(f"Project Root: {project_root}")
# print(f"Python Path: {sys.path.insert(0, project_root)}")

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from api import routers

# from app.config import settings, setup_app_logging
from api.config import (
    API_PROJECT_NAME,
    API_V1_STR,
    __version__,
    settings,
    setup_app_logging,
)
from api.db import models
from api.db.database import engine

# setup logging as early as possible
setup_app_logging(config=settings)

# Prefix for all API endpoints
preFix: str = API_V1_STR
api_project_name: str = API_PROJECT_NAME

app = FastAPI(
    title=f"{api_project_name}",
    openapi_url=f"{preFix}/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    servers=settings.SERVERS,
)

# models.Base.metadata.create_all(bind=engine)

root_router = APIRouter(tags=["Root"])


@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body: str = (
        "<html>"
        "<body style='display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #7d8492;'>"
        "<div style='text-align: center; background-color: white; padding: 20px; border-radius: 20px;'>"
        f"<h1 style='font-weight: bold; font-family: Arial;'>{api_project_name}</h1>"
        f"<h3 style='font-weight: bold; font-family: Arial;'>Version: {__version__}</h3>"
        "<div>"
        f"<h4>Check the docs: <a href='/docs'>here</a><h4>"
        "</div>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


app.include_router(routers.desc_router, prefix=preFix)
app.include_router(routers.auth_router, prefix=preFix)
app.include_router(routers.user_router, prefix=preFix)
app.include_router(routers.post_router, prefix=preFix)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# # Add TrustedHost middleware
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["*.app", "*.example.com"],
# )

# # Add GZip middleware
# app.add_middleware(
#     GZipMiddleware,
#     minimum_size=1000,
# )


if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.FASTAPI_PORT,
        log_level="debug",
        reload=True,
    )

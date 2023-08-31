from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from xray_settings import app as xray_settings_app

from xray_swagger.logging import configure_logging
from xray_swagger.web.api import docs
from xray_swagger.web.api.router import api_router
from xray_swagger.web.auth import router as auth_router
from xray_swagger.web.exception_handlers import register_exception_handlers
from xray_swagger.web.lifetime import register_shutdown_event, register_startup_event
from xray_swagger.web.middlewares import register_middlewares

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="xray_swagger",
        version=metadata.version("xray_swagger"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Adds Exception Handlers
    register_exception_handlers(app)

    # Adds Middlewares
    register_middlewares(app)

    # Main router for the API.
    app.include_router(docs.router)
    app.include_router(router=auth_router, prefix="/auth", tags=["auth"])
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    # Include xray_settings for JSON schema app
    app.mount("/xsettings", xray_settings_app)

    return app

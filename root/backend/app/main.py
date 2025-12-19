from fastapi import FastAPI
from app.core.config import load_settings
from app.core.logging import setup_logging
from app.api.v1.router import router as api_v1_router


def create_app() -> FastAPI:
    setup_logging()
    settings = load_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(
        api_v1_router,
        prefix=settings.api_v1_prefix,
    )

    return app


app = create_app()
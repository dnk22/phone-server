from fastapi import FastAPI

from control_api.api.error_handlers import install_error_handlers
from control_api.api.v1.router import api_router
from control_api.core.config import load_settings


def create_app() -> FastAPI:
    app = FastAPI(title="Control API", version="0.1.0")
    install_error_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()


def run() -> None:
    import uvicorn

    settings = load_settings()
    uvicorn.run("control_api.main:app", host=settings.host, port=settings.port, reload=True)

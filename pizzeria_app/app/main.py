from fastapi import FastAPI

from app.database.connections import create_database
from app.dto.config import generate_config
from app.routes.api import api_router


def create_app() -> FastAPI:
    config = generate_config()

    app = FastAPI(title='Pizzeria APP', description='App for my favorite pizzeria')
    app.state.config = config
    app.state.postgres = create_database(config.postgres)
    app.include_router(api_router)

    return app

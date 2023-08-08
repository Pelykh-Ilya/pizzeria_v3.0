from fastapi import FastAPI


from pizzeria_app.app.routes.api import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app

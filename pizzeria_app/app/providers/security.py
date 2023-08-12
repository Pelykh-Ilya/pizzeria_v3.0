from starlette.requests import Request
from pydantic import BaseModel, SecretStr


class SecurityModel(BaseModel):
    secret_key: str
    token_lifetime: int


def get_secrets(request: Request) -> SecurityModel:
    return SecurityModel(
        secret_key=request.app.state.config.secret_key.get_secret_value(),
        token_lifetime=request.app.state.config.token_lifetime
    )


def get_secret_key(request: Request) -> str:
    return request.app.state.config.secret_key.get_secret_value()


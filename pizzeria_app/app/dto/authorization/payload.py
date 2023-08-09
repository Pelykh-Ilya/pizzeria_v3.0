from pydantic import BaseModel


class AuthorizationPayload(BaseModel):
    username: str
    password: str

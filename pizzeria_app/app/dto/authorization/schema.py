from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuthorizationSchema(BaseModel):
    id: UUID
    username: str
    password: str

    class Config:
        from_attributes = True

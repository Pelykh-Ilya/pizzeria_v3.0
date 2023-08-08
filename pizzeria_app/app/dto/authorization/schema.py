from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Authorization(BaseModel):
    id: UUID
    username: str
    password: str

    class Config:
        orm_mode = True

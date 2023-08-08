from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CustomerSchema(BaseModel):
    id: UUID
    name: str
    address: str
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

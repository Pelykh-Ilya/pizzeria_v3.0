from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PositionsSchema(BaseModel):
    id: UUID
    name: str
    type: str
    quantity: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PositionSchema(BaseModel):
    id: UUID
    name: str
    type: str
    quantity: int
    unit_of_measurement: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Products(BaseModel):
    id: UUID
    name: str
    description: str
    price: int
    units_in_stock: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

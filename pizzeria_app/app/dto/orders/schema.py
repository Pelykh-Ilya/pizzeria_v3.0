from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Orders(BaseModel):

    id: UUID
    customer_id: Optional[UUID]
    total_price: int
    status: bool
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True

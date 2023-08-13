from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Products(BaseModel):
    id: UUID
    name: str
    description: str
    price: int
    units_in_stock: int
    on_stop_list: bool
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

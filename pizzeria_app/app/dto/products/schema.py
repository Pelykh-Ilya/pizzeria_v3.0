from datetime import datetime
from typing import List
from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price: Decimal
    on_stop_list: bool
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class RelatedPosition(BaseModel):
    id: UUID
    name: str
    type: str
    quantity_for_product: int


class ProductWithRelationSchema(ProductSchema):
    related_positions: List[RelatedPosition]

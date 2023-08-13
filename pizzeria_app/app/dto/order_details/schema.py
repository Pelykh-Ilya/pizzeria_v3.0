from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class OrderDetails(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True

from uuid import UUID

from pydantic import BaseModel


class OrderDetails(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: int

    class Config:
        from_attributes = True

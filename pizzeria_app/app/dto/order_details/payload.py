from uuid import UUID

from pydantic import BaseModel


class EditOrderDetailsPayload(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: int


class NewOrderDetailsPayload(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: int


class GetOrderDetailsPayload(BaseModel):
    order_id: UUID
    
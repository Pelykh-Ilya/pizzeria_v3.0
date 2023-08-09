from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EditOrderPayload(BaseModel):
    id: UUID
    customer_id: Optional[UUID]
    total_price: int
    status: bool = False


class NewOrderPayload(BaseModel):
    customer_id: Optional[UUID]
    total_price: int
    status: bool


class GetOrderPayload(BaseModel):
    id: UUID

from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class StatusEnum(str, Enum):
    NEW = "new"
    CHANGED = "changed"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderSchema(BaseModel):
    id: UUID
    customer_id: UUID | None
    total_price: Decimal
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderProductSchema(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: Decimal


class OrderWithDetailsSchema(OrderSchema):
    ordered_products: List[OrderProductSchema]

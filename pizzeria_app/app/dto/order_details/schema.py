from enum import Enum
from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class StatusEnum(str, Enum):
    NEW = "new"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderDetails(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    status: StatusEnum

    class Config:
        from_attributes = True

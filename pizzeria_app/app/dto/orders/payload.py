from enum import Enum
from typing import List
from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class OrderedProductsModel(BaseModel):
    product_id: UUID
    quantity: int


class StatusEnum(str, Enum):
    NEW = "new"
    COMPLETED = "completed"
    CANCELED = "canceled"


class NewOrderPayload(BaseModel):
    customer_id: UUID | None
    ordered_products: List[OrderedProductsModel]


class EditOrderPayload(BaseModel):
    customer_id: UUID | None
    total_price: Decimal | None
    status: StatusEnum
    ordered_products: List[OrderedProductsModel]

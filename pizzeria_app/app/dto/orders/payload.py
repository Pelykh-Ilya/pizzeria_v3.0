from typing import List
from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class OrderProductModel(BaseModel):
    product_id: UUID
    quantity: int


class NewOrderPayload(BaseModel):
    customer_id: UUID | None = None
    ordered_products: List[OrderProductModel]


class EditOrderPayload(BaseModel):
    customer_id: UUID | None = None
    total_price: Decimal | None = None
    ordered_products: List[OrderProductModel]

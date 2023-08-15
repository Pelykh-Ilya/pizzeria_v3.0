from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel


class OrderDetailsPayload(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal


from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class RelatedPositionModel(BaseModel):
    position_id: UUID
    quantity: int


class NewProductPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    related_positions: List[RelatedPositionModel]
    price: Decimal
    description: str | None = None
    on_stop_list: bool = False


class EditProductPayload(BaseModel):
    related_positions: List[RelatedPositionModel] | None = None
    price: Decimal | None = None
    description: str | None = None
    on_stop_list: bool | None = None
    is_active: bool | None = None

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PositionTypeEnum(str, Enum):
    MEAT = "meat"
    SEAFOOD = "seafood"
    CHEESE = "cheese"
    VEGETABLES = "vegetables"
    SOFT_DRINK = "soft drink"
    OTHER = "other"


class PositionUnitEnum(str, Enum):
    ML = "ml"
    GRAM = "gram"
    Piece = "piece"


class NewPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    type: PositionTypeEnum
    unit_of_measurement: PositionUnitEnum


class EditPositionPayload(BaseModel):
    name: str = Field(None, min_length=1, max_length=128)
    is_active: bool | None

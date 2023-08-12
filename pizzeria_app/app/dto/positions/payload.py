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


class NewPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    type: PositionTypeEnum


class EditPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    is_active: bool

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PositionTypeEnum(str, Enum):
    MEAT = "meat"
    CHEESE = "cheese"
    VEGETABLES = "vegetables"


class NewPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    type: PositionTypeEnum


class EditPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    is_active: bool


class GetPositionPayload(BaseModel):
    id: UUID

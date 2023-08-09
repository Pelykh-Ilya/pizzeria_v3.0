from uuid import UUID

from pydantic import BaseModel, Field


class NewPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    type: str = Field(..., min_length=1, max_length=128)
    quantity: int = 0


class GetPositionPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)

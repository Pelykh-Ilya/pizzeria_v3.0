from uuid import UUID

from pydantic import BaseModel


class ProductsPositions(BaseModel):
    product_id: UUID
    position_id: UUID

    class Config:
        from_attributes = True

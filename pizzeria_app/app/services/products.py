from typing import List

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import PositionsModel, ProductsModel
from app.dto.products.payload import RelatedPositionModel, NewProductPayload


async def check_exists_positions(
        positions: List[RelatedPositionModel],
        db: AsyncSession,
):
    position_ids = [position.position_id for position in positions]
    position_stmt = select(PositionsModel.id).where(PositionsModel.id.in_(position_ids))
    exists_positions = await db.scalars(position_stmt)
    exist_positions_result = exists_positions.all()
    if len(position_ids) != len(exist_positions_result):
        difference_position = set(position_ids) - set(exist_positions_result)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Position {difference_position} not represented in db"
        )


async def check_for_exists_product_by_name(
        product_name: str,
        db: AsyncSession,
):
    query = select(ProductsModel).where(ProductsModel.name == product_name)
    if await db.scalar(query):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists",
        )


async def check_new_product_properties(
        new_product_payload: NewProductPayload,
        db: AsyncSession,
):
    await check_for_exists_product_by_name(db=db, product_name=new_product_payload.name)
    await check_exists_positions(db=db, positions=new_product_payload.related_positions)

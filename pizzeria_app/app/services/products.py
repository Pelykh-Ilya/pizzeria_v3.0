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
    position_stmt = select(func.count(PositionsModel.id)).where(PositionsModel.id.in_(position_ids))
    exists_positions = await db.scalar(position_stmt)
    # получать id и выводить недостающие позиции дописать!
    if len(position_ids) != exists_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some position not represented in db"
        )


async def check_for_exists_good_by_name(
        product_name: str,
        db: AsyncSession
):
    query = select(ProductsModel).where(ProductsModel.name == product_name)
    if await db.scalar(query):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exists"
        )


async def check_new_product_properties(
        new_product_payload: NewProductPayload,
        db: AsyncSession
):
    await check_for_exists_good_by_name(db=db, product_name=new_product_payload.name)
    await check_exists_positions(db=db, positions=new_product_payload.related_positions)

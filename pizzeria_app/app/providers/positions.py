import logging
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.payload import PositionTypeEnum
from app.providers.database import get_async_session

logger = logging.getLogger(__name__)


async def get_position_by_id(
        position_id: UUID,
        db: AsyncSession = Depends(get_async_session)
) -> PositionsModel:
    position_query = await db.execute(
        select(PositionsModel).where(PositionsModel.id == position_id)
    )
    if position := position_query.scalar():
        return position
    logger.exception(f"Position with id {position_id} not found")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Position with id {position_id} not found"
    )


async def check_for_position_duplicate(
        position_name: str,
        db: AsyncSession
):
    position_query = await db.execute(
        select(PositionsModel).where(PositionsModel.name == position_name)
    )
    position = position_query.scalar()
    if position:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Position {position_name} is already exist"
        )


async def get_filter_positions(
        db: AsyncSession,
        name: str,
        type: PositionTypeEnum,
        is_active: bool,
        allow_zero_count: bool
):
    positions_query = select(PositionsModel).where(
        PositionsModel.is_active == is_active
    )
    if name:
        positions_query = positions_query.where(PositionsModel.name.ilike(f"{name}%"))
    if type:
        positions_query = positions_query.where(PositionsModel.type == type)
    if not allow_zero_count:
        positions_query = positions_query.where(PositionsModel.quantity > 0)

    logger.info(positions_query)
    positions = await db.execute(positions_query)
    return positions.scalars().all()

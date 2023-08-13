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
    logger.warning(f"Position with id {position_id} not found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Position with id {position_id} not found"
    )

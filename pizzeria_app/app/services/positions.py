from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import PositionsModel


async def check_for_position_duplicate(
        position_name: str,
        db: AsyncSession,
):
    position_query = await db.execute(
        select(PositionsModel).where(PositionsModel.name == position_name)
    )
    position = position_query.scalar()
    if position:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Position {position_name} is already exist"
        )

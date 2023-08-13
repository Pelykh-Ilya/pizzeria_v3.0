from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.payload import EditPositionPayload, PositionTypeEnum


async def edit_position_info(
        db: AsyncSession, position: PositionsModel, edit_position: EditPositionPayload
) -> PositionsModel:
    is_updated = False
    if edit_position.name and edit_position.name != position.name:
        position.name = edit_position.name
        is_updated = True
    if isinstance(edit_position.is_active, bool) and edit_position.is_active != position.is_active:
        position.is_active = edit_position.is_active
        is_updated = True
    if is_updated:
        await db.commit()
        await db.refresh(position)
    return position


async def get_filtered_positions(
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
    positions = await db.execute(positions_query)
    return positions.scalars().all()

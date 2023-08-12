import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.payload import EditPositionPayload

logger = logging.getLogger(__name__)


async def edit_position_info(db: AsyncSession, position: PositionsModel, edit_position: EditPositionPayload):
    is_updated = False
    if edit_position.name and edit_position.name != position.name:
        position.name = edit_position.name
        is_updated = True
    if edit_position.is_active and edit_position.is_active != position.is_active:
        position.is_active = edit_position.is_active
        is_updated = True
    if is_updated:
        await db.commit()
        await db.refresh(position)
        logger.info(f"Position info with id {position.id} updated")
    else:
        logger.info(f"Position info with id {position.id} without changes")
    return position



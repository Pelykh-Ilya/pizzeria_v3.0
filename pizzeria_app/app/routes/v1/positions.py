import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.positions import edit_position_info, get_filtered_positions
from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.payload import NewPositionPayload, PositionTypeEnum, EditPositionPayload
from app.dto.positions.schema import PositionSchema
from app.providers.database import get_async_session
from app.providers.positions import get_position_by_id
from app.security.jwt_token import check_token
from app.services.positions import check_for_exists_position_by_name

logger = logging.getLogger(__name__)
positions_router = APIRouter(prefix="/positions", tags=["Positions"])


@positions_router.post("/", dependencies=[Depends(check_token)], response_model=PositionSchema)
async def create_new_position(
        payload: NewPositionPayload,
        db: AsyncSession = Depends(get_async_session)
):
    await check_for_exists_position_by_name(position_name=payload.name, db=db)
    position = PositionsModel(name=payload.name, type=payload.type, unit_of_measurement=payload.unit_of_measurement)
    db.add(position)
    await db.commit()
    await db.refresh(position)
    logger.debug("Position with name %s created", payload.name)
    return position


@positions_router.get("/search", response_model=List[PositionSchema], dependencies=[Depends(check_token)])
async def get_all_positions(
    name: str | None = None,
    type: PositionTypeEnum | None = None,
    is_active: bool = True,
    allow_zero_count: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    return await get_filtered_positions(
        name=name,
        type=type,
        is_active=is_active,
        allow_zero_count=allow_zero_count,
        db=db,
    )


@positions_router.patch("/{position_id}", dependencies=[Depends(check_token)], response_model=PositionSchema)
async def edit_position(
        payload: EditPositionPayload,
        position: PositionsModel = Depends(get_position_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    await check_for_exists_position_by_name(position_name=payload.name, db=db)
    return await edit_position_info(db=db, position=position, edit_position=payload)


@positions_router.get("/{position_id}", dependencies=[Depends(check_token)], response_model=PositionSchema)
async def get_position(position: PositionsModel = Depends(get_position_by_id)):
    return position

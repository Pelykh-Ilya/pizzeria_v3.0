import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.positions import edit_position_info
from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.payload import NewPositionPayload, PositionTypeEnum, EditPositionPayload, GetPositionPayload
from app.dto.positions.schema import PositionsSchema
from app.providers.database import get_async_session
from app.providers.positions import get_position_by_id, get_filter_positions
from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
positions_router = APIRouter(prefix="/positions", tags=["Positions"])


@positions_router.post("/", dependencies=[Depends(check_token)], response_model=PositionsSchema)
async def create_new_position(
        payload: NewPositionPayload,
        db: AsyncSession = Depends(get_async_session)
):
    position = PositionsModel(name=payload.name, type=payload.type)
    db.add(position)
    await db.commit()
    await db.refresh(position)
    return position


@positions_router.get("/search", response_model=List[PositionsSchema])  # , dependencies=[Depends(check_token)]
async def get_all_positions(
    name: str | None = None,
    type: PositionTypeEnum | None = None,
    is_active: bool = True,
    allow_zero_count: bool = False,
    db: AsyncSession = Depends(get_async_session)
):
    return await get_filter_positions(
        name=name,
        type=type,
        is_active=is_active,
        allow_zero_count=allow_zero_count,
        db=db
    )


@positions_router.patch("/{position_id}", dependencies=[Depends(check_token)], response_model=PositionsSchema)
async def edit_position(
        payload: EditPositionPayload,
        position: PositionsModel = Depends(get_position_by_id),
        db: AsyncSession = Depends(get_async_session)
):
    return await edit_position_info(db=db, position=position, edit_position=payload)


@positions_router.get("/{position_id}", dependencies=[Depends(check_token)], response_model=PositionsSchema)
async def get_position(
        position_id: UUID = Path(...),
        db: AsyncSession = Depends(get_async_session)
):
    return await get_position_by_id(position_id=position_id, db=db)

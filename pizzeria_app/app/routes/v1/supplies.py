from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import PositionsModel
from app.dto.positions.schema import PositionSchema
from app.providers.database import get_async_session
from app.providers.positions import get_position_by_id
from app.security.jwt_token import check_token

supplies_router = APIRouter(prefix="/supplies_write_off", tags=["Supplies, Write off"])


@supplies_router.patch(
    "/supplies/{position_id}",
    dependencies=[Depends(check_token)],
    response_model=PositionSchema
)
async def supplies_position(
        add_quantity: int = Query(..., gt=0),
        position: PositionsModel = Depends(get_position_by_id),
        db: AsyncSession = Depends(get_async_session)
):
    position.quantity += add_quantity
    await db.commit()
    await db.refresh(position)
    return position


@supplies_router.patch(
    "/write_of/{position_id}",
    dependencies=[Depends(check_token)],
    response_model=PositionSchema,
)
async def write_off_position(
        reduce_quantity: int = Query(..., gt=0),
        position: PositionsModel = Depends(get_position_by_id),
        db: AsyncSession = Depends(get_async_session)
):
    if position.quantity > reduce_quantity:
        position.quantity -= reduce_quantity
        await db.commit()
        await db.refresh(position)
        return position
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Current quantity {position.quantity} cannot be written off {reduce_quantity}",
    )


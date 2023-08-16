import logging
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import OrdersModel
from app.providers.database import get_async_session

logger = logging.getLogger(__name__)


async def get_order_by_id(
        order_id: UUID,
        db: AsyncSession = Depends(get_async_session)
) -> OrdersModel:
    order_query = await db.execute(
        select(OrdersModel).where(OrdersModel.id == order_id)
    )
    if order := order_query.scalar():
        return order
    logger.warning("Order with id %s not found", order_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with id {order_id} not found"
    )

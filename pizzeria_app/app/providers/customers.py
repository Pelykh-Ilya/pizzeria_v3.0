import logging
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import CustomersModel
from app.providers.database import get_async_session

logger = logging.getLogger(__name__)


async def get_customer_by_id(
        customer_id: UUID,
        db: AsyncSession = Depends(get_async_session),
) -> CustomersModel:
    customer_query = await db.execute(
        select(CustomersModel).where(CustomersModel.id == customer_id)
    )
    if customer := customer_query.scalar():
        return customer
    logger.warning(f"Customer with id {customer_id} not found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Customer with id {customer_id} not found"
    )


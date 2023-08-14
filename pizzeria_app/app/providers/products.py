import logging
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import ProductsModel
from app.providers.database import get_async_session

logger = logging.getLogger(__name__)


async def get_product_by_id(
        product_id: UUID,
        db: AsyncSession = Depends(get_async_session)
) -> ProductsModel:
    product_query = await db.execute(
        select(ProductsModel).where(ProductsModel.id == product_id)
    )
    if product := product_query.scalar():
        return product
    logger.warning("Position with id %s not found", product_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found"
    )

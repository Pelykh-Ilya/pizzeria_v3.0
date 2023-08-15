import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.orders import create_order
from app.dto.orders.payload import NewOrderPayload
from app.dto.orders.schema import OrderWithDetailsSchema, OrderSchema
from app.providers.database import get_async_session
from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post("/", response_model=OrderSchema)  # , dependencies=[Depends(check_token)]
async def create_new_order(
        payload: NewOrderPayload,
        db: AsyncSession = Depends(get_async_session),
):
    return await create_order(payload=payload, db=db)


@orders_router.get("/search", dependencies=[Depends(check_token)], response_model=List[OrderSchema])
async def get_all_order():
    pass


@orders_router.get("/{order_id}", dependencies=[Depends(check_token)], response_model=OrderWithDetailsSchema)
async def get_order():
    pass


@orders_router.patch("/{order_id}", dependencies=[Depends(check_token)], response_model=OrderWithDetailsSchema)
async def edit_order():
    pass

# роут отмены
# роут выполнения

# в поиске заказаво добавить поиск по продукту
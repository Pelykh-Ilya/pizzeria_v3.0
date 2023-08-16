import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.controllers.orders import create_order, get_order_with_detail, get_filtered_order, edit_order_info, \
    return_positions
from app.database.db_models.pizzeria_tables import OrdersModel
from app.dto.orders.payload import NewOrderPayload, EditOrderPayload
from app.dto.orders.schema import OrderWithDetailsSchema, OrderSchema
from app.providers.database import get_async_session
from app.providers.orders import get_order_by_id
from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post(
    "/",
    response_model=OrderWithDetailsSchema,
    dependencies=[Depends(check_token)],
)
async def create_new_order(
        payload: NewOrderPayload,
        db: AsyncSession = Depends(get_async_session),
):
    return await create_order(payload=payload, db=db)


@orders_router.get(
    "/search",
    dependencies=[Depends(check_token)],
    response_model=List[OrderSchema],
)
async def get_all_order(
        customer_id: UUID | None = None,
        sort_by_price: str | None = Query(None, description="Choose from: 'asc' or 'desc'"),
        order_status: str | None = Query(None, description="Choose from: 'new', 'completed', 'canceled'"),
        product_in_order: str | None = None,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_filtered_order(
        customer_id=customer_id,
        sort_by_price=sort_by_price,
        order_status=order_status,
        product_in_order=product_in_order,
        db=db
    )


@orders_router.patch(
    "/change_status_to_completed/{order_id}",
    dependencies=[Depends(check_token)],
    response_model=OrderWithDetailsSchema,
)
async def change_status_to_completed(
        order: OrdersModel = Depends(get_order_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    if order.status != "canceled":
        order.status = "completed"
        await db.commit()
        await db.refresh(order)
        return await get_order_with_detail(order=order, db=db)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Order with id {order.id} was canceled"
    )


@orders_router.patch(
    "/change_status_to_canceled/{order_id}",
    dependencies=[Depends(check_token)],
    response_model=OrderWithDetailsSchema,
)
async def change_status_to_canceled(
        order: OrdersModel = Depends(get_order_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    order.status = "canceled"
    await db.commit()
    await db.refresh(order)
    await return_positions(order=order, db=db)
    return await get_order_with_detail(order=order, db=db)


@orders_router.patch(
    "/{order_id}",
    dependencies=[Depends(check_token)],
    response_model=OrderWithDetailsSchema,
)
async def edit_order(
        payload: EditOrderPayload,
        order: OrdersModel = Depends(get_order_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    return await edit_order_info(
        edit_order=payload,
        order=order,
        db=db,
    )


@orders_router.get(
    "/{order_id}",
    dependencies=[Depends(check_token)],
    response_model=OrderWithDetailsSchema,
)
async def get_order(
        order: OrdersModel = Depends(get_order_by_id),
        db: AsyncSession = Depends(get_async_session)
):
    return await get_order_with_detail(order=order, db=db)

import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
orders_detail_router = APIRouter(prefix="/orders_detail", tags=["Orders_detail"])


@orders_detail_router.get("/{order_id}")
async def get_order():
    pass


@orders_detail_router.patch("/{order_id}")
async def edit_order():
    pass


@orders_detail_router.post("/new")
async def create_new_order():
    pass

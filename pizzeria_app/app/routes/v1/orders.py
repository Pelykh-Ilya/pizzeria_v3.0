import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/{order_id}")
async def get_order():
    pass


@orders_router.patch("/{order_id}")
async def edit_order():
    pass


@orders_router.get("/list")
async def get_all_order():
    pass


@orders_router.post("/new")
async def create_new_order():
    pass

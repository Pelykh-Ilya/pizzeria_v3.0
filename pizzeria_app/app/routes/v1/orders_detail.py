import logging

from fastapi import APIRouter, Depends

from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
orders_detail_router = APIRouter(prefix="/orders_detail", tags=["Orders_detail"])


@orders_detail_router.get("/{order_id}", dependencies=[Depends(check_token)])
async def get_order():
    pass


@orders_detail_router.patch("/{order_id}", dependencies=[Depends(check_token)])
async def edit_order():
    pass


@orders_detail_router.post("/new", dependencies=[Depends(check_token)])
async def create_new_order():
    pass

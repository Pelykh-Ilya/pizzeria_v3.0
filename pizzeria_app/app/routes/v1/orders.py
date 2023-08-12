import logging

from fastapi import APIRouter, Depends

from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/{order_id}", dependencies=[Depends(check_token)])
async def get_order():
    pass


@orders_router.patch("/{order_id}", dependencies=[Depends(check_token)])
async def edit_order():
    pass


@orders_router.get("/list", dependencies=[Depends(check_token)])
async def get_all_order():
    pass


@orders_router.post("/new", dependencies=[Depends(check_token)])
async def create_new_order():
    pass

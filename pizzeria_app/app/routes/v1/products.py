import logging

from fastapi import APIRouter, Depends

from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.post("/", dependencies=[Depends(check_token)])
async def create_new_product():
    pass


@products_router.patch("/{product_name}", dependencies=[Depends(check_token)])
async def edit_product():
    pass


@products_router.get("/{product_name}", dependencies=[Depends(check_token)])
async def get_product():
    pass


@products_router.get("/list", dependencies=[Depends(check_token)])
async def get_all_products():
    pass


@products_router.delete("/{product_name}", dependencies=[Depends(check_token)])
async def delete_product():
    pass

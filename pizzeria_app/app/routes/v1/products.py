import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.post("/")
async def create_new_product():
    pass


@products_router.patch("/{product_name}")
async def edit_product():
    pass


@products_router.get("/{product_name}")
async def get_product():
    pass


@products_router.get("/list")
async def get_all_products():
    pass


@products_router.delete("/{product_name}")
async def delete_product():
    pass

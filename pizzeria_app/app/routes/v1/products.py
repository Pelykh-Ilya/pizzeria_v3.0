import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.products import create_product
from app.dto.products.payload import NewProductPayload
from app.dto.products.schema import ProductSchema
from app.providers.database import get_async_session
from app.security.jwt_token import check_token
from app.services.products import check_new_product_properties

logger = logging.getLogger(__name__)
products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.post("/", dependencies=[Depends(check_token)], response_model=ProductSchema)
async def create_new_product(
        payload: NewProductPayload,
        db: AsyncSession = Depends(get_async_session)
):
    await check_new_product_properties(new_product_payload=payload, db=db)
    return await create_product(db=db, payload=payload)


@products_router.patch("/{product_id}", dependencies=[Depends(check_token)])
async def edit_product():
    pass


@products_router.get("/{product_id}", dependencies=[Depends(check_token)])
async def get_product():
    pass


@products_router.get("/search", dependencies=[Depends(check_token)])
async def get_all_products():
    pass

import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.products import create_product, edit_product_info, get_filtered_products, get_product_with_relation
from app.database.db_models.pizzeria_tables import ProductsModel, ProductsPositionsModel, PositionsModel
from app.dto.products.payload import NewProductPayload, EditProductPayload
from app.dto.products.schema import ProductSchema, ProductWithRelationSchema, RelatedPosition
from app.providers.database import get_async_session
from app.providers.products import get_product_by_id
from app.security.jwt_token import check_token
from app.services.products import check_new_product_properties, check_exists_positions

logger = logging.getLogger(__name__)
products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.post("/", dependencies=[Depends(check_token)], response_model=ProductSchema)
async def create_new_product(
        payload: NewProductPayload,
        db: AsyncSession = Depends(get_async_session)
):
    await check_new_product_properties(new_product_payload=payload, db=db)
    return await create_product(db=db, payload=payload)


@products_router.get("/search", dependencies=[Depends(check_token)], response_model=List[ProductSchema])
async def get_all_products(
        name: str | None = None,
        ge_price: int | None = None,
        on_stop_list: bool = False,
        is_active: bool = True,
        db: AsyncSession = Depends(get_async_session),
):
    return await get_filtered_products(
        name=name,
        ge_price=ge_price,
        on_stop_list=on_stop_list,
        is_active=is_active,
        db=db,
    )


@products_router.patch("/{product_id}", dependencies=[Depends(check_token)], response_model=ProductSchema)
async def edit_product(
        payload: EditProductPayload,
        product: ProductsModel = Depends(get_product_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    await check_exists_positions(db=db, positions=payload.related_positions)
    return await edit_product_info(db=db, product=product, edit_product=payload)


@products_router.get(
    "/{product_id}",
    dependencies=[Depends(check_token)],
    response_model=ProductWithRelationSchema,
)
async def get_product(product: ProductsModel = Depends(get_product_by_id),
                      db: AsyncSession = Depends(get_async_session)):
    return await get_product_with_relation(db=db, product=product)


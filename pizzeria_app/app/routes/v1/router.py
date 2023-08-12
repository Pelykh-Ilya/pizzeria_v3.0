from fastapi import APIRouter

from app.routes.v1.authorization import authorization_router as authorization
from app.routes.v1.orders import orders_router as orders
from app.routes.v1.orders_detail import orders_detail_router as orders_detail
from app.routes.v1.products import products_router as products
from app.routes.v1.positions import positions_router as position
from app.routes.v1.customers import customers_router as customers

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(authorization)
v1_router.include_router(orders)
v1_router.include_router(orders_detail)
v1_router.include_router(products)
v1_router.include_router(position)
v1_router.include_router(customers)

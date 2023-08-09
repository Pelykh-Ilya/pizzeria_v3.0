import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("/")
async def create_new_customer():
    pass


@customers_router.put("/{customer_phone}")
async def edit_customer():
    pass


@customers_router.get("/{customer_phone}")
async def get_customer():
    pass


@customers_router.get("/")
async def get_customers():
    pass

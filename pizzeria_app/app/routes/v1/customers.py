import logging

from fastapi import APIRouter, Depends

from app.security.jwt_token import check_token

logger = logging.getLogger(__name__)
customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("/", dependencies=[Depends(check_token)])
async def create_new_customer():
    pass


@customers_router.put("/{customer_phone}", dependencies=[Depends(check_token)])
async def edit_customer():
    pass


@customers_router.get("/{customer_phone}", dependencies=[Depends(check_token)])
async def get_customer():
    pass


@customers_router.get("/", dependencies=[Depends(check_token)])
async def get_customers():
    pass

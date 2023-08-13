import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.customers import edit_customer_info, get_filtered_customers
from app.database.db_models.pizzeria_tables import CustomersModel
from app.dto.customers.payload import NewCustomerPayload, EditCustomerPayload
from app.dto.customers.schema import CustomerSchema
from app.providers.customers import get_customer_by_id
from app.providers.database import get_async_session
from app.security.jwt_token import check_token
from app.services.customers import check_customers_duplicate

logger = logging.getLogger(__name__)
customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("/", dependencies=[Depends(check_token)], response_model=CustomerSchema)
async def create_new_customer(
        payload: NewCustomerPayload,
        db: AsyncSession = Depends(get_async_session),
):
    await check_customers_duplicate(customer_phone=payload.phone, db=db)
    customer = CustomersModel(name=payload.name, address=payload.address, phone=payload.phone)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    logger.debug("Customer with phone number %s created", payload.phone)
    return customer


@customers_router.get("/search", response_model=List[CustomerSchema], dependencies=[Depends(check_token)])
async def get_customers(
        name: str | None = None,
        address: str | None = None,
        phone: str | None = None,
        is_active: bool = True,
        db: AsyncSession = Depends(get_async_session),
):
    return await get_filtered_customers(
        name=name,
        address=address,
        phone=phone,
        is_active=is_active,
        db=db
    )


@customers_router.patch(
    "/{customer_id}",
    dependencies=[Depends(check_token)],
    response_model=CustomerSchema
)
async def edit_customer(
        payload: EditCustomerPayload,
        customer: CustomersModel = Depends(get_customer_by_id),
        db: AsyncSession = Depends(get_async_session),
):
    await check_customers_duplicate(customer_phone=payload.phone, db=db)
    return await edit_customer_info(customer=customer, edit_customer=payload, db=db)


@customers_router.get("/{customer_id}", dependencies=[Depends(check_token)], response_model=CustomerSchema)
async def get_customer_by_id(
        customer: CustomersModel = Depends(get_customer_by_id)
):
    return customer

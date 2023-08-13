from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import CustomersModel
from app.dto.customers.payload import EditCustomerPayload


async def edit_customer_info(
        db: AsyncSession, customer: CustomersModel, edit_customer: EditCustomerPayload
) -> CustomersModel:
    is_updated = False
    if edit_customer.name and edit_customer.name != customer.name:
        customer.name = edit_customer.name
        is_updated = True
    if edit_customer.address and edit_customer.address != customer.address:
        customer.address = edit_customer.address
        is_updated = True
    if isinstance(edit_customer.is_active, bool) and edit_customer.is_active != customer.is_active:
        customer.is_active = edit_customer.is_active
        is_updated = True
    if is_updated:
        await db.commit()
        await db.refresh(customer)
    return customer


async def get_filtered_customers(
        db: AsyncSession,
        name: str,
        address: str,
        phone: str,
        is_active: bool = True,
) -> Sequence[CustomersModel]:
    customer_query = select(CustomersModel).where(CustomersModel.is_active == is_active)
    if name:
        customer_query = customer_query.where(CustomersModel.name.ilike(f"%{name}%"))
    if address:
        customer_query = customer_query.where(CustomersModel.address.ilike(f"%{address}%"))
    if phone:
        customer_query = customer_query.where(CustomersModel.phone == phone)
    customers = await db.execute(customer_query)
    return customers.scalars().all()

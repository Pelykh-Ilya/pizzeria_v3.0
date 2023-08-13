from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import CustomersModel


async def check_customers_duplicate(
        customer_phone: str,
        db: AsyncSession,
):
    customers_query = await db.execute(
        select(CustomersModel).where(CustomersModel.phone == customer_phone)
    )
    customer = customers_query.scalar()
    if customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with phone {customer_phone} is already exist"
        )

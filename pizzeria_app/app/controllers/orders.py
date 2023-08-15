from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import OrdersModel, OrderDetailsModel, ProductsModel
from app.dto.orders.payload import NewOrderPayload


async def add_order_details(
        payload: NewOrderPayload,
        order: OrdersModel,
        db: AsyncSession,
):
    order_details = []
    product_ids = [product.product_id for product in payload.ordered_products]
    product_price = await db.scalars(
        select(ProductsModel.price).where(ProductsModel.id.in_(product_ids))
    )
    id_price = {product_id: price for product_id, price in zip(product_ids, product_price.all())}
    for product in payload.ordered_products:
        order_details.append(
            OrderDetailsModel(
                order_id=order.id,
                product_id=product.product_id,
                quantity=product.quantity,
                unit_price=id_price.get(product.product_id,),
            )
        )
    db.add_all(order_details)
    await db.commit()


async def prepare_order_details(
        payload: NewOrderPayload,
        db: AsyncSession
) -> Decimal:
    product_ids = [product.product_id for product in payload.ordered_products]
    product_price = await db.scalars(
        select(ProductsModel.price).where(ProductsModel.id.in_(product_ids))
    )
    # дописать проверку на наличие
    # взять по продукт_ид (ид_позиции, необходмое количесвто для продукта * количество продукта) из продукт_позишин
    # и сравнить с количеством в позициях, если больше то все ок, меньше кидаем ошибку)
    return Decimal(sum(product_price.all()))


async def create_order(
        payload: NewOrderPayload,
        db: AsyncSession
) -> OrdersModel:
    total_price = await prepare_order_details(payload=payload, db=db)
    order = OrdersModel(
        customer_id=payload.customer_id,
        total_price=total_price
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    await add_order_details(payload=payload, db=db, order=order)
    return order

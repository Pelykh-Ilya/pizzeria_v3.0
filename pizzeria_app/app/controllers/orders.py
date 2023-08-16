from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_models.pizzeria_tables import OrdersModel, OrderDetailsModel, ProductsModel, \
    ProductsPositionsModel, PositionsModel
from app.dto.orders.payload import NewOrderPayload, EditOrderPayload, OrderProductModel
from app.dto.orders.schema import OrderWithDetailsSchema, OrderProductSchema


async def _create_mapping_product_id_price(
        payload: NewOrderPayload,
        db: AsyncSession,
) -> dict:
    product_ids = [product.product_id for product in payload.ordered_products]
    product_price = await db.scalars(
        select(ProductsModel.price).where(ProductsModel.id.in_(product_ids))
    )
    id_price = {product_id: price for product_id, price in zip(product_ids, product_price.all())}
    return id_price
#
#
# async def _create_mapping_product_id_quantity(payload: NewOrderPayload) -> dict:
#     product_ids = [product.product_id for product in payload.ordered_products]
#     product_quantity = [product.quantity for product in payload.ordered_products]
#     id_quantity = {product_id: price for product_id, price in zip(product_ids, product_quantity)}
#     return id_quantity


async def _add_order_details(
        payload: NewOrderPayload,
        order: OrdersModel,
        db: AsyncSession,
):
    order_details = []
    id_price = await _create_mapping_product_id_price(payload=payload, db=db)
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


# async def _calculate_total_sum(
#         payload: NewOrderPayload,
#         db: AsyncSession
# ) -> Decimal:
#     id_price = await _create_mapping_product_id_price(payload=payload, db=db)
#     id_quantity = await _create_mapping_product_id_quantity(payload=payload)
#     total_sum = 0
#     for product_id, price in id_price.items():
#         total_sum += price * id_quantity.get(product_id)
#     return Decimal(total_sum)


# async def _create_mapping_position_id_quantity(
#         payload: NewOrderPayload,
#         db: AsyncSession
# ) -> dict:
#     id_quantity_product = await _create_mapping_product_id_quantity(payload=payload)
#     product_ids = [product.product_id for product in payload.ordered_products]
#     quantity_for_product = await db.execute(
#         select(ProductsPositionsModel.product_id,
#                ProductsPositionsModel.position_id,
#                ProductsPositionsModel.quantity_for_product
#                ).where(ProductsPositionsModel.product_id.in_(product_ids))
#     )
#     need_quantity_of_position_for_product_mapping = {}
#     results =
#     for query in :
#         if need_quantity_of_position_for_product_mapping.get(query[1]):
#             need_quantity_of_position_for_product_mapping[query[1]] += query[2] * id_quantity_product.get(query[0])
#         else:
#             need_quantity_of_position_for_product_mapping[query[1]] = query[2] * id_quantity_product.get(query[0])
#     return need_quantity_of_position_for_product_mapping


async def _prepare_order_details(
        product_info: OrderProductModel,
        db: AsyncSession
) -> Decimal:
    product_price = None
    query = (
        select(
            ProductsPositionsModel.quantity_for_product,
            PositionsModel.name,
            PositionsModel.quantity.label("warehouse_quantity"),
            ProductsModel.name.label("product_name"),
            ProductsModel.price
            )
        .join(PositionsModel, PositionsModel.id == ProductsPositionsModel.position_id)
        .join(ProductsModel, ProductsModel.id == ProductsPositionsModel.product_id)
        .where(ProductsPositionsModel.product_id == product_info.product_id)
        )
    result = (await db.execute(query)).all()
    for quantity_for_product, name, warehouse_quantity, product_name, price in result:
        if not product_price:
            product_price = price * product_info.quantity
        if (quantity_for_product * product_info.quantity) > warehouse_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough '{name}' for ordering '{product_name}'"
            )
    return Decimal(product_price)


# async def write_off_positions(
#         payload: NewOrderPayload,
#         db: AsyncSession
# ):
#     need_quantity_of_position_for_product_mapping = await _create_mapping_position_id_quantity(payload=payload, db=db)
#     for position_id, quantity in need_quantity_of_position_for_product_mapping.items():
#         position = await db.scalar(
#             select(PositionsModel).where(PositionsModel.id == position_id)
#         )
#         position -= quantity #
#         await db.commit()
#         await db.refresh(position)


async def get_order_with_detail(order: OrdersModel, db: AsyncSession) -> OrderWithDetailsSchema:
    ordered_products = await db.execute(
        select(OrderDetailsModel.product_id, OrderDetailsModel.quantity, OrderDetailsModel.unit_price
               ).where(OrderDetailsModel.order_id == order.id)
    )
    ordered_product_models = []
    for product in ordered_products.all():
        ordered_product_models.append(OrderProductSchema(
            product_id=product[0],
            quantity=product[1],
            unit_price=product[2]
        ))
    order_with_detail = OrderWithDetailsSchema(
        id=order.id,
        customer_id=order.customer_id,
        total_price=order.total_price,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at,
        ordered_products=ordered_product_models
    )
    return order_with_detail


async def create_order(
        payload: NewOrderPayload,
        db: AsyncSession
) -> OrderWithDetailsSchema:
    total_price = 0
    for product in payload.ordered_products:
        total_price += await _prepare_order_details(db=db, product_info=product)
    order = OrdersModel(
        customer_id=payload.customer_id,
        total_price=total_price
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    await _add_order_details(payload=payload, db=db, order=order)
    # # списать позиции со слада!
    return await get_order_with_detail(order=order, db=db)


async def get_filtered_order(
        customer_id: UUID,
        sort_by_price: str,
        order_status: str,
        product_in_order: str,
        db: AsyncSession
):
    orders_query = select(OrdersModel)
    if customer_id:
        orders_query = orders_query.where(OrdersModel.customer_id == customer_id)
    if order_status:
        orders_query = orders_query.where(OrdersModel.status == order_status)
    if product_in_order:
        orders_query = orders_query.where(OrdersModel.id.in_(
            select(OrderDetailsModel.order_id).join(
                ProductsModel, ProductsModel.id == OrderDetailsModel.product_id
            ).where(ProductsModel.name.ilike(f"%{product_in_order}%"))
        ))
    if sort_by_price == "asc":
        orders_query = orders_query.order_by(asc(OrdersModel.total_price))
    if sort_by_price == "desc":
        orders_query = orders_query.order_by(desc(OrdersModel.total_price))
    orders = await db.execute(orders_query)
    return orders.scalars().all()


async def edit_order_info(
        edit_order: EditOrderPayload,
        order: OrdersModel,
        db: AsyncSession,
) -> OrderWithDetailsSchema:
    is_updated = False
    if edit_order.customer_id and edit_order.customer_id != order.customer_id:
        order.customer_id = edit_order.customer_id
        is_updated = True
    if edit_order.total_price and edit_order.total_price != order.total_price:
        order.total_price = edit_order.total_price
        is_updated = True
    if edit_order.ordered_products:
        # сравнить списки и если есть различия сохранить изменения в order_details
        # убрать/добавить количество ингридиентов
        pass
    if is_updated:
        order.status = "changed"
        await db.commit()
        await db.refresh(order)
    return await get_order_with_detail(order=order, db=db)

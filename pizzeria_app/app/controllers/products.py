from sqlalchemy import select, delete, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import ProductsModel, ProductsPositionsModel, PositionsModel
from app.dto.products.payload import NewProductPayload, EditProductPayload
from app.dto.products.schema import RelatedPosition, ProductWithRelationSchema


async def add_to_products_positions(
        db: AsyncSession,
        payload: NewProductPayload | EditProductPayload,
        product: ProductsModel,
):
    product_positions = []
    for position in payload.related_positions:
        product_positions.append(
            ProductsPositionsModel(
                product_id=product.id,
                position_id=position.position_id,
                quantity_for_product=position.quantity
            )
        )
    db.add_all(product_positions)
    await db.commit()


async def create_product(
        payload: NewProductPayload,
        db: AsyncSession
):
    product = ProductsModel(
            name=payload.name,
            price=payload.price,
            description=payload.description,
            on_stop_list=payload.on_stop_list,
        )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    await add_to_products_positions(
        db=db,
        product=product,
        payload=payload
    )
    return product


async def edit_product_info(
        product: ProductsModel,
        edit_product: EditProductPayload,
        db: AsyncSession,
) -> ProductsModel:
    is_updated = False
    if edit_product.price and edit_product.price != product.price:
        product.price = edit_product.price
        is_updated = True
    if edit_product.description and edit_product.description != product.description:
        product.description = edit_product.description
        is_updated = True
    if isinstance(edit_product.on_stop_list, bool) and edit_product.on_stop_list != product.on_stop_list:
        product.on_stop_list = edit_product.on_stop_list
        is_updated = True
    if isinstance(edit_product.is_active, bool) and edit_product.is_active != product.is_active:
        product.is_active = edit_product.is_active
        is_updated = True
    if edit_product.related_positions:
        remove_stmt = delete(ProductsPositionsModel).where(ProductsPositionsModel.product_id == product.id)
        await db.execute(remove_stmt)
        await db.commit()
        await add_to_products_positions(
            db=db,
            payload=edit_product,
            product=product
        )
    if is_updated:
        await db.commit()
        await db.refresh(product)
    return product


async def get_filtered_products(
        db: AsyncSession,
        name: str,
        sort_by_price: str,
        on_stop_list: bool,
        is_active: bool,
):
    products_query = select(ProductsModel).where(ProductsModel.is_active == is_active)
    if name:
        products_query = products_query.where(ProductsModel.name.ilike(f"%{name}%"))
    if isinstance(on_stop_list, bool):
        products_query = products_query.where(ProductsModel.on_stop_list == on_stop_list)
    if sort_by_price == "asc":
        products_query = products_query.order_by(asc(ProductsModel.price))
    if sort_by_price == "desc":
        products_query = products_query.order_by(desc(ProductsModel.price))
    product = await db.execute(products_query)
    return product.scalars().all()


async def get_product_with_relation(product: ProductsModel, db: AsyncSession):
    related_position = []
    position_query = (
        select(
            ProductsPositionsModel.position_id,
            PositionsModel.name,
            PositionsModel.type,
            ProductsPositionsModel.quantity_for_product,
        ).select_from(
            ProductsPositionsModel
        ).join(PositionsModel, PositionsModel.id == ProductsPositionsModel.position_id
               ).where(ProductsPositionsModel.product_id == product.id))
    result = await db.execute(position_query)
    for position in result.all():
        related_position.append(
            RelatedPosition(
                id=position[0],
                name=position[1],
                type=position[2],
                quantity_for_product=position[3],
            )
        )
    product_with_relation_position = ProductWithRelationSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        on_stop_list=product.on_stop_list,
        created_at=product.created_at,
        updated_at=product.updated_at,
        is_active=product.is_active,
        related_positions=related_position,
    )
    return product_with_relation_position

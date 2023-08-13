from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models.pizzeria_tables import ProductsModel, ProductsPositionsModel
from app.dto.products.payload import NewProductPayload


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
    return product

import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer, func, Text, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase

# какие колонки будут индексироваться???????????????????????????????????
class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4()
    )
    name = Column(VARCHAR(128), nullable=False)
    address = Column(Text, nullable=False, default="pickup")
    phone = Column(VARCHAR(32), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now()
                        )

    orders = relationship("Orders", back_populates="customer", uselist=True)  # ???????????????????????????????


class Orders(Base):
    __tablename__ = "orders"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    customer_id = Column(pg.UUID(True), ForeignKey("customers.id"))
    total_price = Column(Integer)
    status = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now()
                        )

    customer = relationship("Customers", back_populates="orders")  # ??????????????????????????????????
    order_details = relationship("OrderDetails", back_populates="orders")  # ??????????????????????????????????


class OrderDetails(Base):
    __tablename__ = "order_details"
    order_id = Column(pg.UUID(True), ForeignKey("orders.id"), primary_key=True,)
    product_id = Column(pg.UUID(True), ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Integer)

    order = relationship("Orders", back_populates="order_details")
    products = relationship("Products", back_populates="order_details")  # ??????????????????????????????????


class Products(Base):
    __tablename__ = "products"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4()
    )
    name = Column(VARCHAR(128), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    units_in_stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now()
                        )

    products_positions = relationship("ProductsPositions", back_populates="products", uselist=True)  # ????????


class Positions(Base):
    __tablename__ = "positions"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4()
    )
    name = Column(VARCHAR(128), nullable=False, unique=True)
    type = Column(VARCHAR(128), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now()
                        )

    products_positions = relationship("ProductsPositions", back_populates="positions", uselist=True)  # ???????


# Не понимаю каким образом ингредиенты будут добавляться к конкретному продукту
class ProductsPositions(Base):
    __tablename__ = "products_positions"
    product_id = Column(pg.UUID(True), ForeignKey("products.id"), primary_key=True)
    position_id = Column(pg.UUID(True), ForeignKey("positions.id"))

    products = relationship("Products", back_populates="products_positions", uselist=True)  # ?????????????????
    positions = relationship("Positions", back_populates="products_positions", uselist=True)  # ???????????????


class Authorization(Base):
    __tablename__ = "authorization"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4()
    )
    username = Column(VARCHAR(256), nullable=False)
    password = Column(VARCHAR(256), nullable=False)

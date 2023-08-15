import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer, func, Text, DateTime, NUMERIC
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class CustomersModel(Base):
    __tablename__ = "customers"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4()
    )
    name = Column(VARCHAR(128), nullable=False)
    address = Column(Text, nullable=False, default="pickup")
    phone = Column(VARCHAR(32), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now(),
                        )
    is_active = Column(Boolean, default=True)


class OrdersModel(Base):
    __tablename__ = "orders"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    customer_id = Column(pg.UUID(True), ForeignKey("customers.id"), index=True)
    total_price = Column(NUMERIC)
    status = Column(VARCHAR(128), nullable=False, default="new", server_default="new")
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now(),
                        )


class OrderDetailsModel(Base):
    __tablename__ = "order_details"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    order_id = Column(pg.UUID(True), ForeignKey("orders.id"))
    product_id = Column(pg.UUID(True), ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(NUMERIC)


class ProductsModel(Base):
    __tablename__ = "products"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    name = Column(VARCHAR(128), nullable=False, unique=True, index=True)
    description = Column(Text)
    price = Column(NUMERIC, nullable=False)
    on_stop_list = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now(),
                        )
    is_active = Column(Boolean, default=True)


class PositionsModel(Base):
    __tablename__ = "positions"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    name = Column(VARCHAR(128), nullable=False, unique=True, index=True)
    type = Column(VARCHAR(128), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit_of_measurement = Column(VARCHAR(30), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now(),
                        onupdate=func.now(),
                        server_onupdate=func.now(),
                        )
    is_active = Column(Boolean, default=True)


class ProductsPositionsModel(Base):
    __tablename__ = "products_positions"
    product_id = Column(pg.UUID(True), ForeignKey("products.id"), primary_key=True)
    position_id = Column(pg.UUID(True), ForeignKey("positions.id"), primary_key=True)
    quantity_for_product = Column(Integer, nullable=False)


class AuthorizationModel(Base):
    __tablename__ = "authorization"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    username = Column(VARCHAR(256), nullable=False)
    password = Column(VARCHAR(256), nullable=False)

import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship


class Base:
    pass


class Customer(Base):
    __tablename__ = "customers"
    id = Column(
        pg.UUID(True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )

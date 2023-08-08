import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
orders_detail_router = APIRouter(prefix="/orders_detail", tags=["Orders_detail"])

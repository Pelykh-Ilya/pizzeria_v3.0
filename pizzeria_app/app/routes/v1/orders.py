import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
orders_router = APIRouter(prefix="/orders", tags=["Orders"])

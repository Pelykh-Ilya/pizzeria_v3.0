import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
products_router = APIRouter(prefix="/products", tags=["Products"])

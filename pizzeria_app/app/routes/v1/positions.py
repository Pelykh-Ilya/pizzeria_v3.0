import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
positions_router = APIRouter(prefix="/positions", tags=["Positions"])

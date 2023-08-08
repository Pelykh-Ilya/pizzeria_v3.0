import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
authorization_router = APIRouter(prefix="/authorization", tags=["Authorization"])

import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("/")
def create_customer():
    return {"response": "customer created"}

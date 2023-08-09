import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
positions_router = APIRouter(prefix="/positions", tags=["Positions"])


@positions_router.post("/")
async def create_new_position():
    pass


@positions_router.patch("/{position_name}")
async def edit_position():
    pass


@positions_router.get("/{position_name}")
async def get_position():
    pass


@positions_router.get("/list")
async def get_all_positions():
    pass


@positions_router.delete("/{position_name}")
async def delete_position():
    pass

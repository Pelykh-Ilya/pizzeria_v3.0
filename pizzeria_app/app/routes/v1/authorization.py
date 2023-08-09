import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from pizzeria_app.app.dto.authorization.token import TokenSchema
from pizzeria_app.app.dto.authorization.payload import AuthorizationPayload
from pizzeria_app.app.dto.authorization.schema import AuthorizationSchema
from pizzeria_app.app.providers.database import get_async_session
from pizzeria_app.app.database.db_models.pizzeria_tables import AuthorizationModel
from pizzeria_app.app.security.hash_password import hash_password, check_password

logger = logging.getLogger(__name__)
authorization_router = APIRouter(prefix="/authorization", tags=["Authorization"])


@authorization_router.post("/get_token", response_model=TokenSchema)
async def get_token(
        payload: AuthorizationPayload,
        db: AsyncSession = Depends(get_async_session)
):
    auth_info_stmt = select(AuthorizationModel.password).where(AuthorizationModel.username == payload.username)
    user_password = await db.scalar(auth_info_stmt)
    if not user_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if check_password(password=payload.password, hashed_password=user_password):
        return {"token": "token:)"}


@authorization_router.post("/", response_model=AuthorizationSchema)
async def create_new_user(
        new_user: AuthorizationPayload,
        db: AsyncSession = Depends(get_async_session)
):
    user = AuthorizationModel(
        username=new_user.username,
        password=hash_password(new_user.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

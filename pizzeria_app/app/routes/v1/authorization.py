import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.dto.authorization.token import TokenSchema
from app.dto.authorization.payload import AuthorizationPayload
from app.dto.authorization.schema import AuthorizationSchema
from app.providers.database import get_async_session
from app.database.db_models.pizzeria_tables import AuthorizationModel
from app.providers.security import get_secrets, SecurityModel
from app.security.hash_password import hash_password, check_password
from app.security.jwt_token import create_jwt_token, check_token

logger = logging.getLogger(__name__)
authorization_router = APIRouter(prefix="/authorization", tags=["Authorization"])


@authorization_router.post("/get_token", response_model=TokenSchema)
async def get_token(
        payload: AuthorizationPayload,
        db: AsyncSession = Depends(get_async_session),
        security: SecurityModel = Depends(get_secrets)
):
    auth_info_stmt = select(AuthorizationModel.password).where(AuthorizationModel.username == payload.username)
    user_password = await db.scalar(auth_info_stmt)
    if not user_password:
        logger.exception("User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if check_password(password=payload.password, hashed_password=user_password):
        jwt_token = create_jwt_token(
            user=payload.username,
            secret_key=security.secret_key,
            life_time=security.token_lifetime
            )
        return TokenSchema(token=jwt_token)


# @authorization_router.post("/", dependencies=[Depends(check_token)])
# async def create_new_user(
#         new_user: AuthorizationPayload,
#         db: AsyncSession = Depends(get_async_session),
# ):
#     user = AuthorizationModel(
#         username=new_user.username,
#         password=hash_password(new_user.password)
#     )
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user.username

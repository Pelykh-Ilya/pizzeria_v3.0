import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pizzeria_app.app.dto.authorization.token import TokenSchema
from pizzeria_app.app.dto.authorization.payload import AuthorizationPayload
from pizzeria_app.app.dto.authorization.schema import AuthorizationSchema
from pizzeria_app.app.providers.database import get_async_session
from pizzeria_app.app.database.db_models.pizzeria_tables import Authorization

logger = logging.getLogger(__name__)
authorization_router = APIRouter(prefix="/authorization", tags=["Authorization"])


@authorization_router.post("/", response_model=AuthorizationSchema)
async def create_new_user(new_user: AuthorizationPayload,
                          db: AsyncSession = Depends(get_async_session)):
    user = Authorization(username=new_user.username, password=new_user.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@authorization_router.get("/", response_model=TokenSchema)
def get_token() -> TokenSchema:
    pass

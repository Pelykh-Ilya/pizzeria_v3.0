from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request


async def get_async_session(request: Request) -> AsyncSession:
    async with request.app.state.postgres.session as session:
        yield session

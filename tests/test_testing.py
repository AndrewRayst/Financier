from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_testing(async_client: AsyncClient, async_session: AsyncSession) -> None:
    ...

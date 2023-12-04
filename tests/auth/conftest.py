import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.auth.factories import UserFactory
from src.auth.models import UserModel
from src.auth.utils import password_helper


@pytest.fixture(scope="module")
async def user_data() -> UserModel:
    return UserFactory.build()


@pytest.fixture(scope="module")
async def registered_user(user_data: UserModel, async_session: AsyncSession) -> UserModel:
    instance: UserModel = UserModel(
        email=user_data.email,
        hashed_password=password_helper.hash(user_data.hashed_password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    async_session.add(instance)
    await async_session.commit()
    instance.password = user_data.hashed_password
    return instance

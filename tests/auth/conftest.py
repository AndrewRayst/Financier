import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.auth.factories import UserFactory
from src.auth.models import UserModel
from src.auth.utils import password_helper


@pytest.fixture(scope="module")
async def user_data() -> UserModel:
    """
    fixture for creating data of UserModel.
    :return: data of UserModel.
    """
    return UserFactory.build()


@pytest.fixture(scope="module")
async def registered_user(user_data: UserModel, async_session: AsyncSession) -> UserModel:
    """
    fixture for creating and adding user to database.
    :param user_data: object of UserModel.
    :param async_session: an asynchronous session for ORM operations.
    :return: data of UserModel.
    """
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


@pytest.fixture(scope="module")
async def authorized_user(registered_user: UserModel, async_client: AsyncClient) -> UserModel:
    """
    fixture for authorizing user.
    :param registered_user: data of registered user.
    :param async_client: an asynchronous HTTP client.
    :return: data of UserModel.
    """
    response = await async_client.post(
        "/auth/login",
        data={
            "username": registered_user.email,
            "password": registered_user.password,
        }
    )
    registered_user.auth_cookie = response.cookies.get("financier_auth")
    return registered_user

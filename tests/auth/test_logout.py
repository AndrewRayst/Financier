from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel


async def test_logout_without_cookie(
    async_client: AsyncClient, async_session: AsyncSession, authorized_user: UserModel
) -> None:
    """
    checking the user logout process without cookie.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param authorized_user: an authorized user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == authorized_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/logout",
        data={
            "username": authorized_user.email,
            "password": authorized_user.password,
        }
    )

    # status code check
    assert response.status_code == 401


async def test_logout_with_correct_data(
    async_client: AsyncClient, async_session: AsyncSession, authorized_user: UserModel
) -> None:
    """
    checking the user logout process with correct data.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param authorized_user: an authorized user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == authorized_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/logout",
        data={
            "username": authorized_user.email,
            "password": authorized_user.password,
        },
        cookies={
            "financier_auth": authorized_user.auth_cookie,
        }
    )

    # status code check
    assert response.status_code == 204

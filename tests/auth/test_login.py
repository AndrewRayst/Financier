from httpx import AsyncClient
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel


async def test_login_without_email(
    async_client: AsyncClient, async_session: AsyncSession, registered_user: UserModel
) -> None:
    """
    checking the user login process without email.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param registered_user: a registered user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == registered_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/login",
        data={
            "password": registered_user.password,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_login_without_password(
    async_client: AsyncClient, async_session: AsyncSession, registered_user: UserModel
) -> None:
    """
    checking the user login process without password.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param registered_user: a registered user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == registered_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/login",
        data={
            "username": registered_user.email,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_login_without_correct_password(
    async_client: AsyncClient, async_session: AsyncSession, registered_user: UserModel
) -> None:
    """
    checking the user login process without correct password.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param registered_user: a registered user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == registered_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/login",
        data={
            "username": registered_user.email,
            "password": registered_user.password + "123",  # wrong password
        }
    )

    # status code check
    assert response.status_code == 400


async def test_login_without_correct_username(
    async_client: AsyncClient, async_session: AsyncSession, registered_user: UserModel
) -> None:
    """
    checking the user login process without correct username.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param registered_user: a registered user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == registered_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/login",
        data={
            "username": registered_user.email + "a",  # wrong email
            "password": registered_user.password,
        }
    )

    # status code check
    assert response.status_code == 400


async def test_login_with_correct_data(
    async_client: AsyncClient, async_session: AsyncSession, registered_user: UserModel
) -> None:
    """
    checking the user login process without correct data.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param registered_user: a registered user data.
    :return: None
    """
    # getting user before request
    user_query: Select = select(UserModel).where(UserModel.email == registered_user.email)
    assert await async_session.scalar(user_query) is not None

    # sending a request
    response = await async_client.post(
        "/auth/login",
        data={
            "username": registered_user.email,
            "password": registered_user.password,
        }
    )

    # status code check and cookies
    assert response.status_code == 204
    assert isinstance(response.cookies.get("financier_auth"), str)

from datetime import datetime

from httpx import AsyncClient
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserModel


async def test_registration_without_first_name(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    checking the user registration process without first name.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)
    assert user_before is None

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "last_name": user_data.last_name,
            "email": user_data.email,
            "password": user_data.hashed_password,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_registration_without_last_name(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    checking the user registration process without last name.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)
    assert user_before is None

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "first_name": user_data.first_name,
            "email": user_data.email,
            "password": user_data.hashed_password,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_registration_without_email(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    checking the user registration process without email.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)
    assert user_before is None

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "password": user_data.hashed_password,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_registration_without_password(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    checking the user registration process without password.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)
    assert user_before is None

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
        }
    )

    # status code check
    assert response.status_code == 422


async def test_registration_with_correct_data(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    checking the user registration process with correct data.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)
    assert user_before is None

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "password": user_data.hashed_password,
        }
    )

    # status code check
    assert response.status_code == 201

    # getting user
    user_query: Select = select(UserModel).where(UserModel.id == response.json().get("id"))
    user: UserModel = await async_session.scalar(user_query)

    # response body verification
    assert user is not None
    assert user.email == user_data.email
    assert user.first_name == user_data.first_name
    assert user.last_name == user_data.last_name
    assert user.hashed_password != user_data.hashed_password
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_verified is False
    assert isinstance(user.registered_at, datetime)


async def test_registration_twice(
    async_client: AsyncClient, async_session: AsyncSession, user_data: UserModel
) -> None:
    """
    re-validating the user registration process with the correct identical data.
    :param async_client: an asynchronous HTTP client.
    :param async_session: an asynchronous session for ORM operations.
    :param user_data: a user data for registration.
    :return: None
    """
    # getting user before request
    user_query_before: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_before: UserModel = await async_session.scalar(user_query_before)

    # response body verification
    assert user_before is not None
    assert user_before.email == user_data.email
    assert user_before.first_name == user_data.first_name
    assert user_before.last_name == user_data.last_name
    assert user_before.hashed_password != user_data.hashed_password
    assert user_before.is_active is True
    assert user_before.is_superuser is False
    assert user_before.is_verified is False
    assert isinstance(user_before.registered_at, datetime)

    # sending a request
    response = await async_client.post(
        "/auth/register",
        json={
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "password": user_data.hashed_password,
        }
    )

    # status code check
    assert response.status_code == 400

    # getting user
    user_query_after: Select = select(UserModel).where(UserModel.email == user_data.email)
    user_after: UserModel = await async_session.scalar(user_query_after)

    # response body verification
    assert user_after is not None
    assert user_after.email == user_data.email
    assert user_after.first_name == user_data.first_name
    assert user_after.last_name == user_data.last_name
    assert user_after.hashed_password != user_data.hashed_password
    assert user_after.is_active is True
    assert user_after.is_superuser is False
    assert user_after.is_verified is False
    assert isinstance(user_after.registered_at, datetime)

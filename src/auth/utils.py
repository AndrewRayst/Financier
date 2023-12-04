from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserManagerModel, UserModel
from src.database.core import get_session

context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)


async def get_user_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, UserModel)


async def get_user_manager(
    user_db: BaseUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManagerModel, None]:
    yield UserManagerModel(user_db, password_helper)

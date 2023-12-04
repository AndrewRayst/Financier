from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker

from pydantic import EmailStr

from src.database.core import get_session
from src.auth.models import UserModel


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = get_session

    first_name: str = Faker("first_name")
    last_name: str = Faker("last_name")
    email: EmailStr = Faker("email")
    hashed_password: str = Faker("md5")
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

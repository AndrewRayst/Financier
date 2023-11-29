from datetime import datetime

from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src import config
from src.database.models import BaseModel, IDMixin


class UserModel(SQLAlchemyBaseUserTable[int], BaseModel, IDMixin):  # type: ignore
    __tablename__: str = "user"
    first_name: Mapped[str] = mapped_column(String(length=120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=120), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )


class UserManagerModel(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret: str = config.MANAGER_SECRET
    verification_token_secret: str = config.MANAGER_SECRET

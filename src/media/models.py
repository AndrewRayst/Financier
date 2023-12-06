from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, MappedColumn

from src.database.models import BaseModel, IDMixin


class MediaModel(BaseModel, IDMixin):
    __tablename__: str = "media"
    # transaction_id: Mapped[int] = MappedColumn(Integer, ForeignKey("transaction.id"))
    user_id: Mapped[int] = MappedColumn(Integer, ForeignKey("user.id"))
    src: Mapped[str]

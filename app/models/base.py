from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import MetaData
from config import settings

class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention = settings.db.naming_convention
    )
    id: Mapped[int] = mapped_column(primary_key=True)
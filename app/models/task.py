from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from datetime import datetime

from .base import Base

class Task(Base):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("task_statuses.id"),
        nullable=False
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.now()
    )
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    exec_time: Mapped[int] = mapped_column(Integer, nullable=True)


class TaskStatus(Base):
    __tablename__ = "task_statuses"
    title: Mapped[str] = mapped_column(String(32), nullable=False)

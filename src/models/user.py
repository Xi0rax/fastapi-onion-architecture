import uuid
from datetime import datetime, UTC

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, TaskWatcherModel, TaskExecutorModel, TaskModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(UTC)
    )

    authored_tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        foreign_keys="TaskModel.author_id",
        back_populates="author",
    )
    assigned_tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        foreign_keys="TaskModel.assignee_id",
        back_populates="assignee"
    )
    watched_task_links: Mapped[list[TaskWatcherModel]] = relationship(
        "TaskWatcherModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    executed_task_links: Mapped[list[TaskExecutorModel]] = relationship(
        "TaskExecutorModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    watching_tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        secondary="task_watchers",
        viewonly=True,
        back_populates="watchers"
    )
    executing_tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        secondary="task_executors",
        viewonly=True,
        back_populates="executors"
    )

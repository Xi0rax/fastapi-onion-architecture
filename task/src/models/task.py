import uuid
from datetime import datetime, UTC

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task.src.models import BaseModel, TaskExecutorModel, TaskWatcherModel
from task.src.models.enums import task_status_enum


class TaskModel(BaseModel):
    __tablename__ = 'task'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        task_status_enum,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(UTC)
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        nullable=False,
    )
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
    )
    column_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('column.id'),
    )
    sprint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('sprint.id'),
    )
    board_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('board.id'),
    )
    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('group.id'),
    )
    author = relationship('UserModel', foreign_keys=[author_id], back_populates='authored_tasks')
    assignee = relationship('UserModel', foreign_keys=[assignee_id], back_populates='assigned_tasks')
    column = relationship('ColumnModel', back_populates='tasks')
    sprint = relationship('SprintModel', back_populates='tasks')
    board = relationship('BoardModel', back_populates='tasks')
    group = relationship('GroupModel', back_populates='tasks')
    watcher_links: Mapped[list["TaskWatcherModel"]] = relationship(
        "TaskWatcherModel", back_populates="task", cascade="all, delete-orphan")
    executor_links: Mapped[list["TaskExecutorModel"]] = relationship("TaskExecutorModel", back_populates="task",
                                                                     cascade="all, delete-orphan")
    watchers = relationship("UserModel", secondary="task_watchers", viewonly=True)
    executors = relationship("UserModel", secondary="task_executors", viewonly=True)

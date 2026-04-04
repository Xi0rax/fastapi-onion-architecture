import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel, UserModel, TaskModel


class TaskExecutorModel(BaseModel):
    __tablename__ = "task_executors"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True
    )

    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates="executor_links")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="executed_tasks_links")

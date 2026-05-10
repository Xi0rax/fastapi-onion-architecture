import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_service.src.models.base import BaseModel


class BoardModel(BaseModel):
    __tablename__ = "board"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    columns = relationship("ColumnModel", back_populates="board", cascade="all, delete-orphan")
    tasks = relationship("TaskModel", back_populates="board")

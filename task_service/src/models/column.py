import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_service.src.models.base import BaseModel


class ColumnModel(BaseModel):
    __tablename__ = "column"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    board_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("board.id", ondelete="CASCADE"),
                                                nullable=False)

    board = relationship("BoardModel", back_populates="columns")
    tasks = relationship("TaskModel", back_populates="column")

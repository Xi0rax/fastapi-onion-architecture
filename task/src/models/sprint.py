import uuid
from datetime import date

from sqlalchemy import String, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task.src.models import BaseModel


class SprintModel(BaseModel):
    __tablename__ = "sprint"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_sprint_dates"),
    )
    tasks = relationship("TaskModel", back_populates="sprint")

from sqlalchemy import Enum

task_status_enum = Enum(
    "todo",
    "in_progress",
    "done",
    name="task_status"
)

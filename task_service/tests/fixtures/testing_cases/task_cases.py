from uuid import uuid4


VALID_TASK_PAYLOAD = {
    "title": "My Test Task",
    "description": "Description",
    "status": "todo",
    "author_id": str(uuid4()),
    "assignee_id": None,
}
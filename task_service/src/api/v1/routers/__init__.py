__all__ = [
    'v1_board_router',
    'v1_column_router',
    'v1_group_router',
    'v1_sprint_router',
    'v1_task_executor_router',
    'v1_task_router',
    'v1_task_watcher_router',
    'v1_user_info_router',
]

from src.api.v1.routers.board import router as v1_board_router
from src.api.v1.routers.column import router as v1_column_router
from src.api.v1.routers.group import router as v1_group_router
from src.api.v1.routers.sprint import router as v1_sprint_router
from src.api.v1.routers.task import router as v1_task_router
from src.api.v1.routers.task_executor import router as v1_task_executor_router
from src.api.v1.routers.task_watcher import router as v1_task_watcher_router
from src.api.v1.routers.user_info import router as v1_user_info_router

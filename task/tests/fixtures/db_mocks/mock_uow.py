from unittest.mock import AsyncMock, MagicMock

from task.src.utils.unit_of_work import UnitOfWork


def get_mock_uow():
    uow = MagicMock(spec=UnitOfWork)

    uow.is_open = True

    uow.task = AsyncMock()
    uow.user = AsyncMock()
    uow.board = AsyncMock()
    uow.column = AsyncMock()
    uow.group = AsyncMock()
    uow.sprint = AsyncMock()
    uow.task_executor = AsyncMock()
    uow.task_watcher = AsyncMock()

    return uow
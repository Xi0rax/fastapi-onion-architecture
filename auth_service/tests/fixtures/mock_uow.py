from unittest.mock import AsyncMock, MagicMock

from auth_service.src.utils.unit_of_work import UnitOfWork


def get_mock_uow():
    uow = MagicMock(spec=UnitOfWork)
    uow.is_open = True
    uow.user = AsyncMock()
    return uow

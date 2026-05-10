from task_service.src.models import BoardModel
from task_service.src.utils.repository import SqlAlchemyRepository


class BoardRepository(SqlAlchemyRepository[BoardModel]):
    _model = BoardModel

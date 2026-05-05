from task.src.models import BoardModel
from task.src.utils.repository import SqlAlchemyRepository


class BoardRepository(SqlAlchemyRepository[BoardModel]):
    _model = BoardModel

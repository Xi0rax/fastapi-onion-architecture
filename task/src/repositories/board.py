from src.models import BoardModel
from src.utils.repository import SqlAlchemyRepository


class BoardRepository(SqlAlchemyRepository[BoardModel]):
    _model = BoardModel
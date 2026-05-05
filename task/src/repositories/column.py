from src.models import ColumnModel
from src.utils.repository import SqlAlchemyRepository


class ColumnRepository(SqlAlchemyRepository[ColumnModel]):
    _model = ColumnModel
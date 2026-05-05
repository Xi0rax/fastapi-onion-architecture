from task.src.models import ColumnModel
from task.src.utils.repository import SqlAlchemyRepository


class ColumnRepository(SqlAlchemyRepository[ColumnModel]):
    _model = ColumnModel
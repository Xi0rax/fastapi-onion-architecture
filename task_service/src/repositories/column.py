from task_service.src.models import ColumnModel
from task_service.src.utils.repository import SqlAlchemyRepository


class ColumnRepository(SqlAlchemyRepository[ColumnModel]):
    _model = ColumnModel

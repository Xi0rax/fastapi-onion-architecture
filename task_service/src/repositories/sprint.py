from task_service.src.models import SprintModel
from task_service.src.utils.repository import SqlAlchemyRepository


class SprintRepository(SqlAlchemyRepository[SprintModel]):
    _model = SprintModel

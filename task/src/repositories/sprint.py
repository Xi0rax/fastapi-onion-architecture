from task.src.models import SprintModel
from task.src.utils.repository import SqlAlchemyRepository


class SprintRepository(SqlAlchemyRepository[SprintModel]):
    _model = SprintModel
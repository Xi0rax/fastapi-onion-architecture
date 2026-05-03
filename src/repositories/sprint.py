from src.models import SprintModel
from src.utils.repository import SqlAlchemyRepository


class SprintRepository(SqlAlchemyRepository[SprintModel]):
    _model = SprintModel
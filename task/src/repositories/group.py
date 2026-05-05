from src.models import GroupModel
from src.utils.repository import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository[GroupModel]):
    _model = GroupModel
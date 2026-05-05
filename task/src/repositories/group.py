from task.src.models import GroupModel
from task.src.utils.repository import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository[GroupModel]):
    _model = GroupModel
from task_service.src.models import GroupModel
from task_service.src.utils.repository import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository[GroupModel]):
    _model = GroupModel

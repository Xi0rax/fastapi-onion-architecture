from auth_service.src.models.user import UserModel
from auth_service.src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[UserModel]):
    _model = UserModel

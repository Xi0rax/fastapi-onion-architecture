from auth.src.models.user import UserModel
from auth.src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[UserModel]):
    _model = UserModel

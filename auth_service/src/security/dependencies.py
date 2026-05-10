from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_service.src.security.jwt_utils import decode_access_token

bearer_scheme = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    return decode_access_token(credentials.credentials)

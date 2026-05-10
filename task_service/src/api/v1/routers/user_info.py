from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.broker import AuthUserClient

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user_info(
    user_id: UUID4,
    client: AuthUserClient = Depends(),
) -> dict:
    return await client.get_user_info(str(user_id))

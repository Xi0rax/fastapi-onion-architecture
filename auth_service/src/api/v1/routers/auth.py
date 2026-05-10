from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from auth_service.src.api.v1.services.auth import AuthService
from auth_service.src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserInfoResponse, UserResponse
from auth_service.src.security.dependencies import get_current_user_id

router = APIRouter(tags=["auth_service"])


@router.post("/auth_service/register", status_code=HTTP_201_CREATED)
async def register(
        data: RegisterRequest,
        service: AuthService = Depends(),
) -> UserResponse:
    user = await service.register(data)
    return UserResponse.model_validate(user)


@router.post("/auth_service/login", status_code=HTTP_200_OK)
async def login(
        data: LoginRequest,
        service: AuthService = Depends(),
) -> TokenResponse:
    token = await service.login(data)
    return TokenResponse(access_token=token)


@router.get("/user/info/", status_code=HTTP_200_OK)
async def get_user_info(
        user_id: str = Depends(get_current_user_id),
        service: AuthService = Depends(),
) -> UserInfoResponse:
    return UserInfoResponse.model_validate(await service.get_user_info(user_id))


@router.get("/auth_service/users/{user_id}", status_code=HTTP_200_OK)
async def get_user_info_by_id(
        user_id: UUID4,
        service: AuthService = Depends(),
) -> UserInfoResponse:
    return UserInfoResponse.model_validate(await service.get_user_info(user_id))

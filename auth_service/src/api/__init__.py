from fastapi import APIRouter

from auth_service.src.api.v1.routers import v1_auth_router

router = APIRouter()
router.include_router(v1_auth_router, prefix="/v1")

from fastapi import HTTPException
from starlette.status import HTTP_501_NOT_IMPLEMENTED


class CompanyService:
    async def create_company(self, *args, **kwargs):
        raise HTTPException(HTTP_501_NOT_IMPLEMENTED, 'Company service is not implemented in task_service service')

    async def get_company_with_users(self, *args, **kwargs):
        raise HTTPException(HTTP_501_NOT_IMPLEMENTED, 'Company service is not implemented in task_service service')

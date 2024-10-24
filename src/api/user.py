from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.repository.user import UserRepository

router = APIRouter(
    prefix='/api/user',
    tags=['User']
)


@router.get('')
async def get_all_users():
    users = await UserRepository().get_all()
    users_dict = [user.to_dict() for user in users]
    return JSONResponse(status_code=200, content=users_dict)

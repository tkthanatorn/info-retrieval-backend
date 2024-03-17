from fastapi import Request, APIRouter
from util.response import response
from service import auth

user_router = APIRouter()


@user_router.get("")
async def get_user(req: Request):
    try:
        data = await auth.get_user(req.state.user_id)
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)

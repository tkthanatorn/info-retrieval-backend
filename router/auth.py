from fastapi import APIRouter, Response
from pydantic import BaseModel
from loguru import logger

from service import auth
from util.response import response

auth_router = APIRouter()


class RegisterBody(BaseModel):
    username: str
    password: str


class LoginBody(BaseModel):
    username: str
    password: str


@auth_router.post("/register")
async def register(body: RegisterBody, res: Response):
    try:
        await auth.register(body.username, body.password)
        return response(201, None, None)
    except Exception as e:
        return response(400, None, e)


@auth_router.post("/login", status_code=200)
async def login(body: LoginBody, res: Response):
    try:
        token = await auth.login(body.username, body.password)
        result = dict(token=token)
        return response(200, result, None)
    except Exception as e:
        return response(400, None, e)

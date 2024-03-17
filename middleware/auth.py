from fastapi import Request
from util.response import response
from util import jwt


async def authorize_middleware(req: Request, call_next):
    authorization = req.headers.get("Authorization")
    if authorization is None or authorization.replace(" ", "") == "":
        return response(401, None, "Unauthorized")

    parts = authorization.split(" ")
    if len(parts) != 2:
        return response(401, None, "Unauthorized")

    ok, user_id = jwt.verify_jwt(parts[1])
    if not ok:
        return response(401, None, "Unauthorized")

    req.state.user_id = user_id
    return await call_next(req)

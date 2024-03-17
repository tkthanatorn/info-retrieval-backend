from fastapi import Request
from starlette.responses import Response
from util.response import response
from util import jwt
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:
        if req.url.path == "/auth/login" or req.url.path == "/auth/register":
            return await call_next(req)

        authorization = req.headers.get("X-Authorization")
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

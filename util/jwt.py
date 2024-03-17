import os
from jose import jwt, JWTError
import datetime
from loguru import logger


def create_jwt(sub: str) -> str:
    payload = {
        "exp": datetime.datetime.now()
        + datetime.timedelta(days=0, seconds=float(os.getenv("JWT_EXPIRATION"))),
        "iat": datetime.datetime.now(),
        "sub": sub,
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")


# Verify a JWT
def verify_jwt(token) -> tuple[bool, str]:
    try:
        claim = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return True, claim["sub"]
    except JWTError as e:
        logger.error(f"🚨 Invalid token: {e}")
        return False, ""

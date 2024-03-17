from dependency import Registry
from util import hash, jwt


async def register(username: str, password: str):
    hashed_password = hash.generate_hash(password)
    Registry().user_repo.save(username, hashed_password)


async def login(username: str, password: str) -> str:
    user = Registry().user_repo.find_by_username(username)
    if not hash.compare_hash(password, user["hashed_password"]):
        raise ValueError("Invalid password")

    return jwt.create_jwt(username)

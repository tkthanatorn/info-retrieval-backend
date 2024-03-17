from abc import ABC, abstractmethod
import shortuuid
from infra import get_database


class IUserRepo(ABC):
    @abstractmethod
    def save(self, username: str, hashed_password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_username(self, username: str) -> any:
        raise NotImplementedError


class UserRepo(IUserRepo):
    def save(self, username: str, hashed_password: str) -> None:
        db = get_database()
        sql = (
            "INSERT INTO tbl_users (id, username, hashed_password) VALUES (%s, %s, %s)"
        )
        db.cursor().execute(sql, (shortuuid.uuid(), username, hashed_password))
        db.commit()

    def find_by_username(self, username: str):
        cursor = get_database().cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (username,))
        data = cursor.fetchone()
        if data is None:
            raise Exception("User not found")

        return {
            "id": data[0],
            "username": data[1],
            "hashed_password": data[2],
        }

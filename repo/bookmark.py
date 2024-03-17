from abc import ABC, abstractmethod
from infra import get_database
import shortuuid


class IBookmarkRepo(ABC):
    @abstractmethod
    def save(
        self,
        user_id: str,
        recipe_id: int,
        rating: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str, recipe_id: int):
        raise NotImplementedError


class BookmarkRepo(IBookmarkRepo):
    def save(
        self,
        user_id: str,
        recipe_id: int,
        rating: int,
    ) -> None:
        db = get_database()
        sql = "INSERT INTO tbl_bookmarks (id, user_id, recipe_id, rating) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE user_id = VALUES(user_id), recipe_id = VALUES(recipe_id), rating = VALUES(rating)"
        db.cursor().execute(sql, (shortuuid.uuid(), user_id, recipe_id, rating))
        db.commit()

    def find_by_user_id(self, user_id: str) -> any:
        cursor = get_database().cursor()
        cursor.execute("SELECT * FROM tbl_bookmarks WHERE user_id = %s", (user_id,))
        raw = cursor.fetchall()
        data = list()
        for item in raw:
            data.append(
                dict(
                    id=item[0],
                    user_id=item[1],
                    recipe_id=item[2],
                    rating=item[3],
                )
            )
        return data

    def delete(self, user_id: str, recipe_id: int):
        db = get_database()
        sql = "DELETE FROM tbl_bookmarks WHERE user_id = %s AND recipe_id = %s"
        db.cursor().execute(sql, (user_id, recipe_id))
        db.commit()

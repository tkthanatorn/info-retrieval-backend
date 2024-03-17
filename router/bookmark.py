from fastapi import APIRouter, Depends
from pydantic import BaseModel
from service import bookmark
from util.response import response

bookmark_router = APIRouter()


class SaveBookmarkBody(BaseModel):
    user_id: str
    recipe_id: int
    rating: int


class DeleteBookmarkBody(BaseModel):
    user_id: str
    recipe_id: int


@bookmark_router.post("")
def save(body: SaveBookmarkBody):
    try:
        bookmark.save(body.user_id, body.recipe_id, body.rating)
        return response(201, None, None)
    except Exception as e:
        return response(400, None, e)


@bookmark_router.delete("")
def delete(body: DeleteBookmarkBody):
    try:
        bookmark.delete(body.user_id, body.recipe_id)
        return response(200, None, None)
    except Exception as e:
        return response(400, None, e)


@bookmark_router.get("/{user_id}")
def get_user_bookmarks(user_id: str):
    try:
        result = bookmark.find_by_user_id(user_id)
        return response(200, result, None)
    except Exception as e:
        return response(400, None, e)

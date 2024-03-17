from fastapi import APIRouter
from loguru import logger

from service import recipe
from util.response import response

recipe_router = APIRouter()


@recipe_router.get("")
async def get_recipes(page: int = 0):
    try:
        data = await recipe.get_recipes(page)
        data = [dict(item) for item in data]
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)


@recipe_router.get("/by-name")
async def search_recipe_by_name(query: str):
    try:
        data = await recipe.search_recipe_by_name(query)
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)


@recipe_router.get("/by-instruction")
async def search_recipe_by_instruction(query: str):
    try:
        data = await recipe.search_recipe_by_instruction(query)
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)


@recipe_router.get("/by-ingredient")
async def search_recipe_by_ingredient(query: str):
    try:
        data = await recipe.search_recipe_by_ingredient(query)
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)


@recipe_router.get("/{recipe_id}")
async def get_recipe(recipe_id: int):
    try:
        data = await recipe.get_recipe(recipe_id)
        return response(200, data, None)
    except Exception as e:
        return response(400, None, e)

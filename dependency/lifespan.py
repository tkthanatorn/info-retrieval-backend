from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
import pickle
import pandas as pd

from model import build_bm25_model, build_cleaned_data
from .registry import Registry
from repo.user import UserRepo
from repo.bookmark import BookmarkRepo


@asynccontextmanager
async def lifespan(app: FastAPI):
    build_cleaned_data()
    build_bm25_model()

    Registry().user_repo = UserRepo()
    Registry().bookmark_repo = BookmarkRepo()
    Registry().recipe_df = pd.read_parquet("data/cleaned_recipes.parquet")
    Registry().bm25_recipe_name = pickle.load(open("data/bm25_recipe_name.pkl", "rb"))
    Registry().bm25_recipe_instruction = pickle.load(
        open("data/bm25_recipe_instruction.pkl", "rb")
    )
    Registry().bm25_recipe_ingredient = pickle.load(
        open("data/bm25_recipe_ingredient.pkl", "rb")
    )
    logger.info("🚀 start application")

    yield
    logger.info("💤 shutdown")

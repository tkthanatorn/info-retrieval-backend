from .singleton import SingletonMeta
import pandas as pd
from repo.user import IUserRepo
from repo.bookmark import IBookmarkRepo
from model import BM25


class Registry(metaclass=SingletonMeta):
    user_repo: IUserRepo
    bookmark_repo: IBookmarkRepo
    bm25_recipe_name: BM25
    bm25_recipe_instruction: BM25
    bm25_recipe_ingredient: BM25
    recipe_df: pd.DataFrame

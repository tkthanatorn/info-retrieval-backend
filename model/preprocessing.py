import pandas as pd
import os
import string
import re
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from loguru import logger


def preprocess(ps: PorterStemmer, stop_dict: dict, s: str) -> str:
    s = re.sub("[^A-Za-z]", " ", s)
    s = word_tokenize(s)
    s = [w for w in s if w not in stop_dict]
    s = [ps.stem(w) for w in s]
    s = " ".join(s)
    s = s.translate(str.maketrans("", "", string.punctuation + "\xa0"))
    return s


def build_cleaned_data():
    path = "data/cleaned_recipes.parquet"
    if os.path.exists(path):
        logger.info("✅ cleaned_recipes.parquet already exists")
        return

    def camel_to_snake(name: str) -> str:
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    df = pd.read_parquet("data/recipes.parquet")
    df.columns = [camel_to_snake(col) for col in df.columns]
    df = df[
        [
            "recipe_id",
            "name",
            "description",
            "recipe_instructions",
            "recipe_ingredient_quantities",
            "recipe_ingredient_parts",
            "images",
        ]
    ]

    df.columns = [
        "id",
        "name",
        "description",
        "instructions",
        "ingredient_quantities",
        "ingredient_parts",
        "images",
    ]

    ps = PorterStemmer()
    stopwords_set = set(stopwords.words("english"))
    stop_dict = {s: 1 for s in stopwords_set}

    # cleaned instruction
    df["cleaned_name"] = df["name"].apply(lambda x: preprocess(ps, stop_dict, x))

    # cleaned instruction
    df["cleaned_instruction"] = df["instructions"].apply(lambda x: "".join(x))
    df["cleaned_instruction"] = df["cleaned_instruction"].apply(
        lambda x: preprocess(ps, stop_dict, x)
    )

    # cleaned ingredient
    df["cleaned_ingredient"] = df["ingredient_parts"].apply(lambda x: ",".join(x))
    df["cleaned_ingredient"] = df["cleaned_ingredient"].apply(
        lambda x: preprocess(ps, stop_dict, x)
    )

    df.to_parquet("data/cleaned_recipes.parquet")
    logger.info("✅ cleaned_recipes.parquet builded")

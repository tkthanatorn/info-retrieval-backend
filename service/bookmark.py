from dependency import Registry


def save(user_id: str, recipe_id: int, rating: int) -> None:
    if rating <= 0 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")
    Registry().bookmark_repo.save(user_id, recipe_id, rating)


def delete(user_id: str, recipe_id: int) -> None:
    Registry().bookmark_repo.delete(user_id, recipe_id)


def find_by_user_id(user_id: str) -> any:
    bookmarks = Registry().bookmark_repo.find_by_user_id(user_id)
    df = Registry().recipe_df.copy()
    df = df[df["id"].isin([item["recipe_id"] for item in bookmarks])]
    df["rating"] = df["id"].apply(
        lambda x: next(
            (item["rating"] for item in bookmarks if item["recipe_id"] == x), None
        )
    )
    df.sort_values("rating", ascending=False, inplace=True)

    data = df.to_dict(orient="records")
    for i, item in enumerate(data):
        data[i]["id"] = int(item["id"])
        data[i]["instructions"] = list(item["instructions"])
        data[i]["ingredient_parts"] = list(item["ingredient_parts"])
        data[i]["ingredient_quantities"] = list(item["ingredient_quantities"])
        data[i]["images"] = list(item["images"])
    return data

from dependency import Registry


async def get_recipes(page: int):
    page = max(0, page)
    limit = 12
    data = (
        Registry()
        .recipe_df.iloc[page * limit : (page + 1) * limit]
        .to_dict(orient="records")
    )

    for i, item in enumerate(data):
        data[i]["id"] = int(item["id"])
        data[i]["instructions"] = list(item["instructions"])
        data[i]["ingredient_parts"] = list(item["ingredient_parts"])
        data[i]["ingredient_quantities"] = list(item["ingredient_quantities"])
        data[i]["images"] = list(item["images"])

    return data


async def get_recipe(recipe_id: int):
    df = Registry().recipe_df
    df = df[df["id"] == recipe_id]
    if df.empty:
        raise ValueError(f"Recipe with id {recipe_id} not found")

    data = df.iloc[0].to_dict()
    data["id"] = int(data["id"])
    data["instructions"] = list(data["instructions"])
    data["ingredient_parts"] = list(data["ingredient_parts"])
    data["ingredient_quantities"] = list(data["ingredient_quantities"])
    data["images"] = list(data["images"])
    return data


async def search_recipe_by_name(name: str):
    score = Registry().bm25_recipe_name.transform(name)
    df = Registry().recipe_df.copy()
    df["score"] = score
    df = df.nlargest(n=10, columns="score")
    df.sort_values(by="score", ascending=False, inplace=True)
    data = df.iloc[:10].to_dict(orient="records")

    for i, item in enumerate(data):
        data[i]["id"] = int(item["id"])
        data[i]["instructions"] = list(item["instructions"])
        data[i]["ingredient_parts"] = list(item["ingredient_parts"])
        data[i]["ingredient_quantities"] = list(item["ingredient_quantities"])
        data[i]["images"] = list(item["images"])

    return data


async def search_recipe_by_instruction(instruction: str):
    score = Registry().bm25_recipe_instruction.transform(instruction)
    df = Registry().recipe_df.copy()
    df["score"] = score
    df = df.nlargest(n=10, columns="score")
    df.sort_values(by="score", ascending=False, inplace=True)
    data = df.iloc[:10].to_dict(orient="records")

    for i, item in enumerate(data):
        data[i]["id"] = int(item["id"])
        data[i]["instructions"] = list(item["instructions"])
        data[i]["ingredient_parts"] = list(item["ingredient_parts"])
        data[i]["ingredient_quantities"] = list(item["ingredient_quantities"])
        data[i]["images"] = list(item["images"])

    return data


async def search_recipe_by_ingredient(ingredient: str):
    score = Registry().bm25_recipe_ingredient.transform(ingredient)
    df = Registry().recipe_df.copy()
    df["score"] = score
    df = df.nlargest(n=10, columns="score")
    df.sort_values(by="score", ascending=False, inplace=True)
    data = df.iloc[:10].to_dict(orient="records")

    for i, item in enumerate(data):
        data[i]["id"] = int(item["id"])
        data[i]["instructions"] = list(item["instructions"])
        data[i]["ingredient_parts"] = list(item["ingredient_parts"])
        data[i]["ingredient_quantities"] = list(item["ingredient_quantities"])
        data[i]["images"] = list(item["images"])

    return data

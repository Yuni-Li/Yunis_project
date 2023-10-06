from mongoconfig import CLIENT, DBNAME
from helper import stringify_recipe

def search_recipe_by_name(recipe_name, meal_type, sort_by):
    '''
    Find certain recipes by the given recipe_name
    return the recipes which has the name matched the pattern
    of recipe_name
    '''
    db = CLIENT[DBNAME]
    recipes_col = db['recipes']

    # result stores recipes that there name includes the recipe_name 
    # without caring the upper/lower case
    result = []
    for r in recipes_col.find():
        if recipe_name.lower() in r['name'].lower():
            result.append(stringify_recipe(r))

    # Sorted_result needs to be sorted by the given sort_by parameters
    if sort_by == None:
        sorted_result = sorted(result, key=lambda d: len(d['name'])) 
    elif sort_by == 'likes':
        sorted_result = sorted(result, key=lambda d: d['number_of_likes'], reverse=True)
    elif sort_by == 'ratings':
        sorted_result = sorted(result, key=lambda d: d['rating'], reverse=True)

    # Don't need to include the meal_type, filter it out
    filtered_recipe = sorted_result
    if meal_type != None:
        filtered_recipe = list(filter(lambda recipe: recipe['category'] == meal_type, filtered_recipe))

    return {
        'recipes': filtered_recipe
    }

def search_recipe_by_ingredients(ingredients, meal_type, sort_by): # Given list of ingredients names
    '''
    Find certain recipes by the given ingredients
    '''
    db = CLIENT[DBNAME]
    recipes_col = db['recipes']

    # Matched recipes including those missing some given ingredients
    # completely_matched_recipes stores recipes that given ingredients cover all their ingredients
    # missing_ingredients_recipes stores recipes that given ingredients only cover some of their ingredients
    # but still missing some.
    # The missing ingredients will be stored in all_missing_ingredients
    completely_matched_recipes = []
    missing_ingredients_recipes = []
    all_missing_ingredients = []

    for recipe in recipes_col.find():
        recipe_ingredients_dicts = recipe['ingredients']
        recipe_ingredients = [recipe_ingredient_dict['IngredientName'] for recipe_ingredient_dict in recipe_ingredients_dicts]
        is_missing, missing_ingredients = missing_ingredients_recipe(ingredients, recipe_ingredients)
        if ingredients_match_recipe(ingredients, recipe_ingredients):
            if meal_type != None and recipe['category'] != meal_type:
                continue
            new_recipe = stringify_recipe(recipe)
            new_recipe['missing_ingredients'] = []
            completely_matched_recipes.append(new_recipe)
        elif is_missing:
            if meal_type != None and recipe['category'] != meal_type:
                continue
            all_missing_ingredients += missing_ingredients
            new_recipe = stringify_recipe(recipe)
            new_recipe['missing_ingredients'] = missing_ingredients
            missing_ingredients_recipes.append(new_recipe)
    all_missing_ingredients = list(set(all_missing_ingredients))
    # missing_ingredients is gonna be sorted by number of missing ingredients no matter
    # what sort_by is
    sorted_missing_ingredients_recipes = sorted(missing_ingredients_recipes, key=lambda recipe: len(recipe['missing_ingredients']))
    
    # Completely_matched_recipes needs to be sorted by the given sort_by parameters
    if sort_by == 'ratings':
        completely_matched_recipes = sorted(completely_matched_recipes, key=lambda recipe: recipe['rating'], reverse=True)
    elif sort_by == 'likes':
        completely_matched_recipes = sorted(completely_matched_recipes, key=lambda recipe: recipe['number_of_likes'] ,reverse=True)
    elif sort_by != None:
        return {
            'error': 'no such sorting method'
        }

    # Combine completely_matched_recipes and sorted_missing_ingredients_recipes as matched_recipes to be returned
    matched_recipes = completely_matched_recipes + sorted_missing_ingredients_recipes
    filtered_matched_recipes = matched_recipes
    if len(filtered_matched_recipes) == 0:
        update_ingredients_search_freq(ingredients)

    return {
        'matched_recipes': filtered_matched_recipes, # List of dictionaries
        'missing_ingredients': all_missing_ingredients, # Just name
    }

# Helper functions for searching
def ingredients_match_recipe(ingredients, recipe_ingredients):
    '''
    Check if the ingredients match the recipe has the recipe_ingredients
    '''
    ingredients_set = set(ingredients)
    recipe_ingredients_set = set(recipe_ingredients)
    return ingredients_set.issuperset(recipe_ingredients_set)

def missing_ingredients_recipe(ingredients, recipe_ingredients):
    '''
    Check if the ingredients match the recipe has the recipe_ingredients
    that missing ingredients given
    return bool, missing_ingredients <-- tuple: (boolean, list of ingredient name)
    '''
    ingredients_set = set(ingredients)
    recipe_ingredients_set = set(recipe_ingredients)
    return ingredients_set.issubset(recipe_ingredients_set), list(recipe_ingredients_set.difference(ingredients_set))

def update_ingredients_search_freq(ingredients):
    '''
    Update the frequency(count) of given ingredient being searched
    '''
    db = CLIENT[DBNAME]
    searched_freq_col = db['searched_freq']

    ingredients = sorted(ingredients, key=lambda ingredient: ingredient)
    target_ingredients_key = searched_freq_col.find_one({
        'ingredients_key': ingredients
    })
    if target_ingredients_key == None:
        # Create an ingredients key and set count as 1
        searched_freq_col.insert_one({
            'ingredients_key': ingredients,
            'count': 1
        })
    else:
        count = target_ingredients_key['count']
        count += 1
        # Update count
        searched_freq_col.update_one(
            {
                'ingredients_key': ingredients
            },
            {
                '$set': {
                    'count': count
                }
            }
        )
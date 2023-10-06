from mongoconfig import CLIENT, DBNAME

def select_ingredient(name):
    '''
    Given a name, return the ingredient dict
    '''
    db = CLIENT[DBNAME]
    ingredients_col = db['ingredients']

    target_ingredient = None
    for ingredient in ingredients_col.find():
        for ingredient_dict in ingredient['matched_ingredients']:
            if ingredient_dict['name'] == name:
                target_ingredient = ingredient_dict
                target_ingredient['category'] = ingredient['category']
                return target_ingredient

    # Raise error if ingredient name not found
    return {
        'error': 'ingredient does not exist'
    }

def populate_ingredient(name, category):
    '''
    Creates the ingredients given the name and category 
    and stores the ingredients into the database according to its category
    '''
    db = CLIENT[DBNAME]
    ingredients_col = db['ingredients']

    # Check if the ingredient already exists
    for ingredients in ingredients_col.find():
        for ingredient_dict in ingredients['matched_ingredients']:
            if ingredient_dict['name'] == name:
                return {
                    'error': 'ingredient already exists'
                }

    # create ingredient by provider
    ingredients_dict = {
        'name': name,
        'count': 0,
    }

    ingredient_category = ingredients_col.find_one({
        'category': category,
    })
    if ingredient_category == None:
        # Create a new category dict
        category_dict = {
            'category': category,
            'matched_ingredients': [ingredients_dict],
        }
        ingredients_col.insert_one(category_dict)
    else:
        # Create an ingredient in the category dict
        ingredients_list = ingredient_category['matched_ingredients']
        ingredients_list.append(ingredients_dict)
        ingredients_col.update_one(
            {
                'category': category,
            },
            {
                '$set': {
                    'matched_ingredients': ingredients_list
                }
            }
        )

    return {
        'success': True
    }

def get_ingredients():
    db = CLIENT[DBNAME]
    ingredients_col = db['ingredients']

    # Get ingredients
    ingredients_detail = list(ingredients_col.find())
    for ingredient in ingredients_detail:
        ingredient['_id'] = str(ingredient['_id'])

    return {
        'ingredients': ingredients_detail
    }

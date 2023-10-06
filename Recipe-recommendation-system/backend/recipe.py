from multiprocessing.sharedctypes import Value
from pickle import OBJ
from urllib.parse import uses_query
from mongoconfig import CLIENT, DBNAME
from bson.objectid import ObjectId
from helper import stringify_recipe

def create_recipe(user_id, token, name, image, category, ingredients, description):
    '''
    Create recipe
    Initialized with given parameters
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Find the user by the given user id and token   
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token,
    })
    if target_user == None:
        print('error: you are not the authorized user')
        return {
            'success': False
        }

    # Initialize recipe data into database
    recipes_col = db['recipes']
    recipe_dict = {
        'name': name,
        'image': image,
        'category': category,
        'ingredients': ingredients,
        'description': description,
        'created_by': ObjectId(user_id),
        'number_of_likes': 0,
        'liked_by': [], # List of user_ids (users who likes the recipe)
        'number_of_collections': 0,
        'collected_by': [], # List of user_ids (users who collectes the recipe)
        'rating': 0,
        'number_of_rating': 0,
        'comments': [] # List of comments (comments left by user in recipe)
    }
    insert_result = recipes_col.insert_one(recipe_dict)

    # insert recipe_id into user data
    user_recipes = target_user['recipes']
    recipe_id = insert_result.inserted_id
    user_recipes.append(recipe_id)

    # Update user collection
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            '$set': {
                '_id': ObjectId(user_id),
                'recipes': user_recipes
            }
        }
    )
    recipe_id = str(recipe_id)

    return {
        'recipe_id': recipe_id
    }

def recipe_delete(user_id, token, recipe_id):
    '''
    Delete recipe with the given recipe_id
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'invalid user id'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the authorized user exists
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    if target_user == None:
        return {
            'error': 'user does not exist'
        }

    # Check if the given user is active
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token,
    })
    if target_user == None:
        return {
            'error': 'authorized user is not online'
        }

    # Check validity of object id
    try:
        ObjectId(recipe_id)
    except:
        return {
            'error': 'invalid recipe id'
        }

    # Found recipe by given recipe_id
    recipes_col = db['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        return {
            'error': 'recipe does not exist'
        }

    # Check if the recipe with the given id is created by target_user
    if target_recipe['created_by'] != ObjectId(user_id):
        return {
            'error': 'authorized user is not allowed to delete this recipe'
        }

    # Remove recipe from recipes collection and recipe ID from user's recipe list
    recipes_list = target_user['recipes']
    recipes_list.remove(ObjectId(recipe_id))
    recipes_col.delete_one({
        '_id': ObjectId(recipe_id)
    })

    # Update users recipe list (recipes created by given user)
    users_col.update_one(
        {
            '_id': ObjectId(user_id)
        },
        {
            "$set": {
                'recipes': recipes_list
            }
        }
    )

    # Remove recipe from users' collection
    collected_by_list = target_recipe['collected_by']
    for target_user_id in collected_by_list:
        target_user = users_col.find_one({
            '_id': ObjectId(target_user_id)
        })
        collections = target_user['collections']
        collections.remove(ObjectId(recipe_id))

        # Update users colletion
        users_col.update_one(
            {
                '_id': ObjectId(target_user_id),
            },
            {
                '$set': {
                    'collections': collections
                }
            }
        )

    return {
        'success': True
    }
    
def list_recipes():
    '''
    List all recipes
    '''
    db = CLIENT[DBNAME]
    recipes_col = db['recipes']

    recipes = list(recipes_col.find())
    recipes_name = []
    for recipe in recipes:
        recipe_name = {
            'name': recipe['name']
        }
        if recipe_name not in recipes_name:
            recipes_name.append(recipe_name)

    return {
        'recipes': recipes_name
    }

def show_own_recipes(user_id):
    '''
    List users' recipes
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the authorized user exists
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
    })
    if target_user == None:
        return {
            'error': 'user does not exist'
        }

    user_recipes_id = target_user['recipes']
    user_recipes = []
    # Find recipe from database
    recipes_col = db['recipes']
    for recipe_id in user_recipes_id:
        target_recipe = recipes_col.find_one({
            '_id': recipe_id
        })
        if target_recipe:
            user_recipes.append(stringify_recipe(target_recipe))

    return {
        'recipes': user_recipes
    }

def like_recipe(user_id, token, recipe_id):
    '''
    Like a recipe by a user
    Add the user_id in 'liked_by' of the recipe data with the recipe_id
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token
    })
    if target_user == None:
        print('error: user is not active or authorized')
        return {
            'success': False
        }

    recipes_col = db['recipes']
    # Check if the recipe with given recipe_id exists
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        print('error: no such recipe exists')
        return {
            'success': False
        }

    # Check if the given user has already liked the recipe
    liked_by_list = target_recipe['liked_by']
    number_of_likes = target_recipe['number_of_likes']
    if ObjectId(user_id) in liked_by_list:
        print('error: user has already liked this recipe')
        return {
            'success': False
        }

    # Update database
    liked_by_list.append(ObjectId(user_id))
    number_of_likes += 1
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id),
        },
        {
            '$set': {
                'liked_by': liked_by_list,
                'number_of_likes': number_of_likes
            }
        }
    )

    return {
        'success': True
    }

def unlike_recipe(user_id, token, recipe_id):
    '''
    Unlike a recipe by a user
    Remove the user_id in 'liked_by' of the recipe data with the recipe_id
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token
    })
    if target_user == None:
        print('error: user is not active or authorized')
        return {
            'success': False
        }

    # Check if the recipe with given recipe_id exists
    recipes_col = db['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        print('error: no such recipe exists')
        return {
            'success': False
        }

    # Check if the given user has already liked the recipe
    liked_by_list = target_recipe['liked_by']
    number_of_likes = target_recipe['number_of_likes']
    if ObjectId(user_id) not in liked_by_list:
        print('error: user has not liked this recipe yet')
        return {
            'success': False
        }

    # Update database
    liked_by_list.remove(ObjectId(user_id))
    number_of_likes -= 1
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id)
        },
        {
            '$set': {
                'liked_by': liked_by_list,
                'number_of_likes': number_of_likes
            }
        }
    )

    return {
        'success': True
    }

def rate_recipe(user_id, token, rating, recipe_id):
    '''
    User gives a rating score for the specific recipe
    Update rating score of the recipe data
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']
    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token
    })
    if target_user == None:
        print('error: user is not active or authorized')
        return {
            'success': False
        }

    # Check if the recipe with given recipe_id exists
    recipes_col = db['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        print('error: no such recipe exists')
        return {
            'success': False
        }

    # Update the rating score of target_recipe
    score = target_recipe['rating']
    number_of_rating = target_recipe['number_of_rating']
    total_score = score * number_of_rating + float(rating)
    number_of_rating += 1
    score = total_score / number_of_rating

    # Update database
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id),
        },
        {
            '$set': {
                'rating': score,
                'number_of_rating': number_of_rating,
            }
        }
    )

    return {
        'success': True
    }

def collect_recipe(user_id, token, recipe_id):
    '''
    Collect a recipe by a user
    Updtate 'collections' in user data and 'number_of_collections' in recipe data
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token
    })
    if target_user == None:
        print('error: user is not active or authorized')
        return {
            'success': False
        }

    # Check if the recipe with given recipe_id exists
    recipes_col = db['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        print('error: no such recipe exists')
        return {
            'success': False
        }

    # Check if the given recipe has already collected by the user
    collections_list = target_user['collections']
    collected_by_list = target_recipe['collected_by']
    if ObjectId(recipe_id) in collections_list:
        print('error: user has already collected this recipe')
        return {
            'success': False
        }
    if ObjectId(user_id) in collections_list:
        print('error: user has already collected this recipe')
        return  {
            'success': False
        }

    # Update the collection list and num of collections of target_recipe
    collections_list.append(ObjectId(recipe_id))
    collected_by_list.append(ObjectId(user_id))
    number_of_collections = target_recipe['number_of_collections']
    number_of_collections += 1

    # Update database
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            '$set': {
                'collections': collections_list,
            }
        }
    )
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id),
        },
        {
            '$set': {
                'collected_by': collected_by_list,
                'number_of_collections': number_of_collections,
            }
        }
    )

    return {
        'success': True
    }

def uncollect_recipe(user_id, token, recipe_id):
    '''
    Uncollect a recipe by a user
    Updtate 'collections' in user data and 'number_of_collections' in recipe data
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
    })
    if target_user == None:
        return {
            'error': 'user does not exist'
        }

    # Check if the given user is active
    target_user = users_col.find_one({
        'token': token
    })
    if target_user == None:
        return {
            'error': 'user is not online'
        }

    recipes_col = db['recipes']
    # Check if the recipe with given recipe_id exists
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        print('error: no such recipe exists')
        return {
            'success': False
        }

    # Check if the given recipe has already collected by the user
    collections_list = target_user['collections']
    collected_by_list = target_recipe['collected_by']
    if ObjectId(recipe_id) not in collections_list:
        print('error: user has not collected this recipe yet')
        return {
            'success': False
        }
    if ObjectId(user_id) not in collected_by_list:
        print('error: user has not collected this recipe yet')
        return {
            'success': False
        }

    # Update the collection list and num of collections of target_recipe
    collections_list.remove(ObjectId(recipe_id))
    collected_by_list.remove(ObjectId(user_id))
    number_of_collections = target_recipe['number_of_collections']
    number_of_collections -= 1

    # Update database
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            '$set': {
                'collections': collections_list,
            }
        }
    )
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id),
        },
        {
            '$set': {
                'collected_by': collected_by_list,
                'number_of_collections': number_of_collections,
            }
        }
    )

    return {
        'success': True
    }

def recipe_detail(recipe_id):
    # Check validity of object id
    try:
        ObjectId(recipe_id)
    except:
        return {
            'error': 'recipe does not exist!'
        }

    db = CLIENT[DBNAME]
    recipes_col = db['recipes']

    # Check if the user is active or authorized
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        return {
            'error': 'recipe does not exist'
        }

    # Return the recipe as the type of string
    target_recipe = stringify_recipe(target_recipe)
    return target_recipe

def recipe_comment(user_id, token, recipe_id, comment):
    '''
    User makes a comment in a recipe
    '''
    # Check validity of object id
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'invalid user ID'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user is active or authorized
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    if target_user == None:
        return {
            'error': 'user does not exist'
        }
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token,
    })
    if target_user == None:
        return {
            'error': 'user is not online'
        }

    # Find recipe with recipe_id
    try:
        ObjectId(recipe_id)
    except:
        return {
            'error': 'invalid recipe ID'
        }
    recipes_col = db['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    if target_recipe == None:
        return {
            'error': 'recipe does not exist'
        }

    # Update the comment list of target_recipe 
    # (only remains the newest 5 comments)
    comment_list = target_recipe['comments']
    comment_list.insert(0, comment)
    if len(comment_list) >= 5:
        comment_list = comment_list[:5]

    # Update database
    recipes_col.update_one(
        {
            '_id': ObjectId(recipe_id),
        },
        {
            '$set': {
                'comments': comment_list,
            }
        }
    )
    
    return {
        'success': True
    }

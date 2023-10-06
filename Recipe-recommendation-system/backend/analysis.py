from mongoconfig import CLIENT, DBNAME
from bson.objectid import ObjectId

def get_five_most_followers_users(user_id, token):
    '''
    Get details of the five users who have the most followers
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the given user authorized
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
            'error': 'user is not online'
        }

    # top_five_users stores the details of the five users
    top_five_users = []
    for user in users_col.find():
        user_dict = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'username': user['username'],
            'followers': len(user['followers'])
        }
        top_five_users = insert_top_user(top_five_users, user_dict)

    return {
        'top_five_users': top_five_users
    }

def get_five_most_collection_recipes(user_id, token):
    '''
    Get details of the five recipes which have the most collections 
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']
    recipes_col = db['recipes']

    # Check if the given user authorized
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
            'error': 'user is not online'
        }

    # top_five_recipes stores the details of the five recipes
    top_five_recipes = []
    for recipe in recipes_col.find():
        recipe_dict = {
            'recipe_id': str(recipe['_id']),
            'recipe_name': recipe['name'],
            'collections': recipe['number_of_collections'],
        }
        top_five_recipes = insert_top_recipe(top_five_recipes, recipe_dict)

    return {
        'top_five_recipes': top_five_recipes
    }

def get_ten_most_frequently_searched_set_of_ingredients(user_id, token):
    '''
    Get the ingredients and their frequency which have been searched most  
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']
    searched_freq_col = db['searched_freq']

    # Check if the given user authorized
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
            'error': 'user is not online'
        }
    
    # top_searched_freqs stores the ingredients and their frequency
    top_searched_freqs = []
    for searched_freq in searched_freq_col.find():
        searched_freq_dict = {
            'ingredients_set': searched_freq['ingredients_key'],
            'count': searched_freq['count']
        }
        top_searched_freqs = insert_top_searched_freq(top_searched_freqs, searched_freq_dict)
    return {
        'top_ten_ingredients': top_searched_freqs
    }


# Helper functions for analysis.py
def insert_top_user(users, top_user):
    '''
    Insert top user to the users list,
    and sort it by comparing the number of followers,
    '''
    is_inserted = False
    for i in range(len(users)):
        if top_user['followers'] > users[i]['followers']:
            users.insert(i, top_user)
            is_inserted = True
            break

    if not is_inserted:
        users.append(top_user)

    # If length of the list is greater than 5, pop out last user in the list
    if len(users) > 5:
        users.pop(-1)

    return users

def insert_top_recipe(recipes, top_recipe):
    '''
    Insert top recipe to the recipes list,
    and sort it by comparing the number of collections,
    '''
    is_inserted = False
    for i in range(len(recipes)):
        if top_recipe['collections'] > recipes[i]['collections']:
            recipes.insert(i, top_recipe)
            is_inserted = True
            break

    if not is_inserted:
        recipes.append(top_recipe)

    # If length of the list is greater than 5, pop out last recipe in the list
    if len(recipes) > 5:
        recipes.pop(-1)

    return recipes

def insert_top_searched_freq(searched_freqs, top_searched_freq):
    '''
    Insert top searched frequences to the searched_freqs list,
    and sort it by comparing the count of being searched
    '''
    is_inserted = False
    for i in range(len(searched_freqs)):
        if top_searched_freq['count'] > searched_freqs[i]['count']:
            searched_freqs.insert(i, top_searched_freq)
            is_inserted = True
            break

    if not is_inserted:
        searched_freqs.append(top_searched_freq)

    # If length of the list is greater than 10, pop out last searched frequences in the list
    if len(searched_freqs) > 10:
        searched_freqs.pop(-1)

    return searched_freqs

from mongoconfig import DBNAME, CLIENT

'''
The functions in this file are only for admin use, users won't be
able to call these functions
'''
def get_users():
    '''
    Get all users details from database
    return a list of users details
    '''
    users_col = CLIENT[DBNAME]['users']
    users_details = list(users_col.find())

    for user in users_details:
        user['_id'] = str(user['_id'])
        for i in range(len(user['recipes'])):
            user['recipes'][i] = str(user['recipes'][i])
        for i in range(len(user['followers'])):
            user['followers'][i] = str(user['followers'][i])
        for i in range(len(user['followings'])):
            user['followings'][i] = str(user['followings'][i])
        for i in range(len(user['collections'])):
            user['collections'][i] = str(user['collections'][i])
    return users_details

def clear_users():
    '''
    Delete all users from database
    '''
    users_col = CLIENT[DBNAME]['users']
    users_col.delete_many({})
    return {
        'success': True
    }

def clear_recipes():
    '''
    Delete all recipes from the database
    '''
    recipes_col = CLIENT[DBNAME]['recipes']
    recipes_col.delete_many({})

    return {
        'success': True
    }

def clear_ingredients():
    '''
    Delete all ingredients from database
    '''
    ingredients_col = CLIENT[DBNAME]['ingredients']
    ingredients_col.delete_many({})

    return {
        'success': True
    }

def clear_data():
    '''
    Delete all datas from database
    '''
    clear_users()
    clear_recipes()
    clear_ingredients()

    return {
        'success': True
    }
import re
from check import check_email
from check import check_name
from check import check_password
from mongoconfig import CLIENT, DBNAME
from bson.objectid import ObjectId
import hashlib
from helper import stringify_recipe

def show_profile(user_id):
    '''
    Show all the details of the user with given id
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

    # User with user_id not exists if target_user is None
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    if target_user == None:
        return {
            'error': 'user does not exist!'
        }

    # Change all ObjectId to string
    target_user['_id'] = str(target_user['_id'])

    collections = target_user['collections']
    for i in range(len(collections)):
        collections[i] = str(collections[i])

    followers = target_user['followers']
    for i in range(len(followers)):
        followers[i] = str(followers[i])

    followings = target_user['followings']
    for i in range(len(followings)):
        followings[i] = str(followings[i])

    recipes = target_user['recipes']
    for i in range(len(recipes)):
        recipes[i] = str(recipes[i])

    return {
        'profile': target_user
    }


def change_email(user_id, token, old_email, new_email):
    '''
    Change the email of the user with given id
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

    # Check if the user exist or online
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })

    # User with user_id not exists if target_user is None
    if target_user == None:
        return {
            'error': 'user does not exist'
        }
    target_user = users_col.find_one({
        'token': token
    })

    # User is offline if target_user is None
    if target_user == None:
        return {
            'error': 'user is not online'
        }

    # Check if the new email has been registed
    all_users = users_col.find()
    for user in all_users:
        if user['email'] == new_email:
            return {
                'error': 'Email has been registered'
            }

    # Update user's email
    users_col.update_one(
        {
            'email': old_email,
        },
        {
            '$set': {
                'email': new_email
            }
        }
    )

    return {
        'success': True
    }

def change_username(user_id, token, new_name):
    '''
    Change the username of the user with given id
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

    # Check if the user exist or online
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })

    # User with user_id not exists if target_user is None
    if target_user == None:
        raise ValueError('Error: User does not exist!')
    target_user = users_col.find_one({
        'token': token
    })

    # User is offline if target_user is None
    if target_user == None:
        return {
            'error': 'User is not online'
        }

    # Update user's name
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            '$set': {
                'username': new_name
            }
        }
    )

    return {
        'success': True
    }


def change_password(user_id, token, old_password, new_password):
    '''
    Change the password of the user with given id
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

    # Check if the user exist or online
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })

    # User with user_id not exists if target_user is None
    if target_user == None:
        return {
            'error': 'User does not exist'
        }
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'token': token
    })

    # User is offline if target_user is None
    if target_user == None:
        return {
            'error': 'User does not exist'
        }

    # Old password is not correct if target_user is None
    hashed_old_password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
    target_user = users_col.find_one({
        '_id': ObjectId(user_id),
        'hashed_password': hashed_old_password,
    })
    if target_user == None:
        return {
            'error': 'Old password is not correct'
        }

    # Update user's password
    hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            '$set': {
                'hashed_password': hashed_new_password
            }
        }
    )

    return {
        'success': True
    }


def change_icon(user_id, token, icon):
    '''
    Change the icon of the user with given id
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

    # Check if the user exist or online
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })

    # User with user_id not exists if target_user is None
    if target_user == None:
        raise ValueError('Error: User does not exist!')
    target_user = users_col.find_one({
        'token': token
    })

    # User is offline if target_user is None
    if target_user == None:
        return {
            'error': 'User is not online'
        }

    # Update user's icon
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
        },
        {
            "$set": {
                'icon': icon
            }
        }
    )

    return {
            'success': True
        }


def follow_user(curr_user_id, token, tar_user_id):
    '''
    Current user follows target user
    '''
    # Check validity of object id
    try:
        ObjectId(curr_user_id)
    except:
        return {
            'error': 'user does not exist!'
        }
    try:
        ObjectId(tar_user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user exist or online
    curr_user = users_col.find_one({
        '_id': ObjectId(curr_user_id)
    })

    # User with user_id not exists if curr_user is None
    if curr_user == None:
        return {
            'error': 'user does not exist!'
        }
    curr_user = users_col.find_one({
        '_id': ObjectId(curr_user_id),
        'token': token
    })

    # User is offline if curr_user is None
    if curr_user == None:
        return {
            'error': 'user is not online'
        }
    tar_user = users_col.find_one({
        '_id': ObjectId(tar_user_id)
    })
    if tar_user == None:
        return {
            'error': 'user does not exist'
        }
    
    # Current user id should not be equal to target user id
    if curr_user_id == tar_user_id:
        return {
            'error': "you can't unfollow yourself!"
        }

    # Add target user to current user's following list 
    # Add current user to target user's follower list
    following_list = curr_user['followings']
    follower_list = tar_user['followers']
    if ObjectId(tar_user_id) not in following_list and ObjectId(curr_user_id) not in follower_list:
        following_list.append(ObjectId(tar_user_id))
        follower_list.append(ObjectId(curr_user_id))
    else:
        return {
            'success': False
        }

    # Update curent user's following list
    users_col.update_one(
        {
            '_id': ObjectId(curr_user_id)
        },
        {
            "$set": {
                'followings': following_list
            }
        }
    )

    # Update target user's follower list
    users_col.update_one(
        {
            '_id': ObjectId(tar_user_id)
        },
        {
            "$set": {
                'followers': follower_list
            }
        }
    )

    return {
        'success': True
    }

def unfollow_user(curr_user_id, token, tar_user_id):
    '''
    Current user unfollows target user
    '''
    # Check validity of object id
    try:
        ObjectId(curr_user_id)
    except:
        return {
            'error': 'user does not exist!'
        }
    try:
        ObjectId(tar_user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check if the user exist or online
    curr_user = users_col.find_one({
        '_id': ObjectId(curr_user_id)
    })

    # User with user_id not exists if curr_user is None
    if curr_user == None:
        return {
            'error': 'user does not exist!'
        }
    curr_user = users_col.find_one({
        '_id': ObjectId(curr_user_id),
        'token': token
    })

    # User is offline if curr_user is None
    if curr_user == None:
        return {
            'error': 'user is not online'
        }
    tar_user = users_col.find_one({
        '_id': ObjectId(tar_user_id)
    })
    if tar_user == None:
        return {
            'error': 'user does not exist'
        }
    
    # Current user id should not be equal to target user id
    if curr_user_id == tar_user_id:
        return {
            'error': "you can't unfollow yourself!"
        }

    # Remove target user from current user's following list 
    # Remove current user from target user's follower list
    following_list = curr_user['followings']
    follower_list = tar_user['followers']
    if ObjectId(tar_user_id) in following_list and ObjectId(curr_user_id) in follower_list:
        following_list.remove(ObjectId(tar_user_id))
        follower_list.remove(ObjectId(curr_user_id))
    else:
        return {
            'success': False
        }

    # Update current user's following list
    users_col.update_one(
        {
            '_id': ObjectId(curr_user_id)
        },
        {
            "$set": {
                'followings': following_list
            }
        }
    )

    # Update target user's follower list
    users_col.update_one(
        {
            '_id': ObjectId(tar_user_id)
        },
        {
            "$set": {
                'followers': follower_list
            }
        }
    )

    return {
        'success': True
    }

def is_following(curr_user_id, tar_user_id):
    '''
    Helper function for check if target user is followed by current user
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']

    # Find the users by user_id
    curr_user = users_col.find_one({
        '_id': ObjectId(curr_user_id)
    })
    tar_user = users_col.find_one({
        'u_id': ObjectId(tar_user_id)
    })

    # Return true if target user is in current user's following list and 
    # current user is in target user's follower list
    following_list = curr_user['followings']
    follower_list = tar_user['followers']
    if ObjectId(tar_user_id) in following_list and ObjectId(curr_user_id) in follower_list:
        return True

    return False
 
def show_collection(user_id, token):
    '''
    Show all the collections of the user with the given id
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

    # Check if the user exist or online
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })

    # User with user_id not exists if target_user is None
    if target_user == None:
        raise ValueError('Error: User does not exist!')
    target_user = users_col.find_one({
        'token': token
    })

    # User is offline if target_user is None
    if target_user == None:
        return {
            'error': 'User is not online'
        }
    
    collection_details = show_collection_details(target_user['collections'])
    return collection_details
    
def show_collection_details(collection):
    '''
    Show all the collection details of the user with the given id
    '''
    db = CLIENT[DBNAME]
    recipe_col = db['recipes']

    result = []
    for c in collection:
        target = recipe_col.find_one({
        '_id': ObjectId(c)
        })
        if target != None:
            target = stringify_recipe(target)
            result.append(target)
            
    return result

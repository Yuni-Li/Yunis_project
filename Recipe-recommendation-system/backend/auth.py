from mongoconfig import CLIENT, DBNAME
from bson.objectid import ObjectId
import hashlib

def register(email, username, password, confirmed_password):
    '''
    User register
    Add a new user into database
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']
    all_users = users_col.find()

    # Check if the given email or username has been taken
    for user in all_users:
        if user['email'] == email:
            return {
                'error': 'email has been registered'
            }

    # Check if the password and confirmed_password are the same
    if password != confirmed_password:
        return {
            'error': 'your passwords are not the same'
        }

    # Hash the password and store the generated token in user details
    token = hashlib.sha224(password.encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Initialize user details into database
    user_dict = {
        'email': email,
        'username': username,
        'hashed_password': hashed_password,
        'token': token, # user will have logged in after successfully registered
        'icon': '', # image url?
        'recipes': [], # List of recipe_ids (recipes created by the user)
        'followers' : [], # List of user_ids (users following the user)
        'followings': [], # List of user_ids (users followed by the user)
        'collections': [], # List of recipe_ids (recipes collected by the user)
    }
    insert_result = users_col.insert_one(user_dict)
    user_id = str(insert_result.inserted_id)

    return {
        'user_id': user_id,
        'token': token
    }

def login(email, password):
    '''
    User login
    Update the login user token
    '''
    db = CLIENT[DBNAME]
    users_col = db['users']

    # Check whether there is a user in database with the same input email
    target_user = users_col.find_one({
        'email': email,
    })
    if target_user == None:
        return {
            'error': 'email does not belong to a user'
        }
        
    # Check if the hashed password and the user token stored in the database are the same
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if target_user['hashed_password'] != hashed_password:
        return {
            'error': 'password is not correct'
        }

    # Set the user as active, user logged in
    token = hashlib.sha224(password.encode('utf-8')).hexdigest() # Will be changed by using hash function

    # Check if the user is active
    if target_user['token'] == token:
        return {
            'error': 'user is already online'
        }

    # Check if the token is valid
    if target_user['token'] != '':
        return {
            'error': 'invalid token'
        }

    # Update users database
    user_id = str(target_user['_id'])
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
            'token': ''
        },
        {
            '$set': {
                'token': token
            }
        }
    )

    return {
        'user_id': user_id,
        'token': token
    }

def logout(user_id, token):
    '''
    User logout
    Set the given active user token as empty string
    '''
    # Check if the given user authorized
    try:
        ObjectId(user_id)
    except:
        return {
            'error': 'user does not exist!'
        }

    # Find the user by the given user id and token
    db = CLIENT[DBNAME]
    users_col = db['users']
    target_user = users_col.find_one(
        {
            '_id': ObjectId(user_id),
            'token': token
        }
    )
    if target_user == None:
        return {
            'success': False
        }

    # Update users database
    users_col.update_one(
        {
            '_id': ObjectId(user_id),
            'token': token,
        },
        {
            '$set': {
                '_id': ObjectId(user_id),
                'token': '',
            }
        },
    )
    
    return {
        'success': True
    }

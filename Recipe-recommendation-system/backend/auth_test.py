import auth
import admin
from mongoconfig import CLIENT, DBNAME
from bson.objectid import ObjectId


def test_register():
    admin.clear_data()
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # Check if the given user in database
    users_col = CLIENT[DBNAME]['users']
    user_detail = users_col.find_one({
        'email': 'sample.user@gmail.com',
        '_id': ObjectId(user_id),
        'token': token,
    })
    assert user_detail != None

def test_logout():
    admin.clear_data()
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # Check if the given user in database
    users_col = CLIENT[DBNAME]['users']
    user_detail = users_col.find_one({
        'email': 'sample.user@gmail.com',
        '_id': ObjectId(user_id),
        'token': token,
    })
    print(token)
    assert user_detail != None
    status = auth.logout(user_id, token)
    # Check logout success
    assert status['success']
    # Check user token is empty
    user_detail = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert user_detail != None
    assert user_detail['token'] == ''

def test_login():
    admin.clear_data()
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # Check if the given user in database
    users_col = CLIENT[DBNAME]['users']
    user_detail = users_col.find_one({
        'email': 'sample.user@gmail.com',
        '_id': ObjectId(user_id),
        'token': token,
    })
    print(token)
    assert user_detail != None
    status = auth.logout(user_id, token)
    # Check logout success
    assert status['success']
    # Check user token is empty
    user_detail = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert user_detail != None
    assert user_detail['token'] == ''
    
    # Login
    user_detail = auth.login('sample.user@gmail.com', 'sampleuser123')
    user_id = user_detail['user_id']
    token = user_detail['token']
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert target_user['token'] == token


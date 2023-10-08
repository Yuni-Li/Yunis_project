from channel_data import data
from error import InputError, AccessError

def clear():
    '''
    Clears the User's/channel's data
    Resets the internal data of the application to it's initial state
    '''
    global data
    data.clear()
    ## Make them EMPTY
    data['users'] = []
    data['channels'] = []

def users_all(token):
    users = []
    for i in data['users']:
        dic = {}
        dic['u_id'] = i['u_id']
        dic['email'] = i['email']
        dic['name_first'] = i['name_first']
        dic['name_last'] = i['name_last']
        dic['handle_str'] = i['handle_str']
        users.append(dic)
    return {
        'users': users
    }

def admin_userpermission_change(token, u_id, permission_id):
    valid_uid = False
    is_owner = False
    # u_id of token
    token_id = 0
    for i in data['users']:
        if i['u_id'] == u_id:
            valid_uid = True
            break
    
    if not valid_uid:
        raise InputError('Invalid user id')

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']
            break

    for i in data['users']:
        if i['u_id'] == token_id:
            if i['permission_id'] == 1:
                is_owner = True
                break

    if not is_owner:
        raise AccessError('You are not an owner')

    for i in data['users']:
        if i['u_id'] == u_id:
            i['permission_id'] = permission_id
            break
    
    return {}

def search(token, query_str):
    l = []
    token_id = 0

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']
            break
    
    for i in data['channels']:
        for j in i['messages']:
            if j['u_id'] == token_id:
                l.append(j)

    return {
        'messages': l
    }
from channel_data import data
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    valid_uid = False
    valid_chid = False
    valid_auth = False  # check if authorised user is in channel
    already_member = False
    channel_index = 0
    user_index = 0
    # u_id of token
    token_id = 0
    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            channel_index = i
            valid_chid = True
            break
    
    for i in range(len(data.get('users'))):
        if data.get('users')[i].get('u_id') == u_id:
            user_index = i
            valid_uid = True
            break
    
    if (not valid_uid) or (not valid_chid):
        raise InputError('Input invalid user id or channel id!')

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            valid_auth = True
            break
    
    if (not valid_auth):
        raise AccessError('Unable to invite!')

    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == u_id:
            already_member = True
            break
    
    if already_member:
        raise InputError('The invited user is already a member!')

    dic = {
        'u_id': data.get('users')[user_index]['u_id'],
        'name_first': data.get('users')[user_index]['name_first'],
        'name_last': data.get('users')[user_index]['name_last'],
    }
    
    data.get('channels')[channel_index].get('all_members').append(dic)

    return {
    }

def channel_details(token, channel_id):
    valid_chid = False
    valid_auth = False  # check if authorised user is in channel
    channel_index = 0
    token_id = 0

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError('Invalid channel id!')

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            valid_auth = True
            break
    
    if not valid_auth:
        raise AccessError('You are not a member of this channel!')

    name = data.get('channels')[channel_index].get('name')
    owner = data.get('channels')[channel_index].get('owner_members')
    member = data.get('channels')[channel_index].get('all_members')

    L = {'name': name, 'owner_members': owner, 'all_members': member,}
    return L

def channel_messages(token, channel_id, start):
    valid_chid = False
    valid_auth = False
    channel_index = 0
    token_id = 0

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")
    
    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            valid_auth = True
            break
    
    if not valid_auth:
        raise AccessError('You are not a member of this channel!')

    if start > len(data.get('channels')[channel_index].get('messages')):
        raise InputError("Invalid start!")

    end = 0
    
    if start + 50 > len(data.get('channels')[channel_index].get('messages')):
        end = len(data.get('channels')[channel_index].get('messages'))
    else:
        end = start + 50

    l = []
    for i in range(start, end):
        l = [data.get('channels')[channel_index].get('messages')[i]] + l
    
    if start + 50 > len(data.get('channels')[channel_index].get('messages')):
        end = -1
    
    RETURN = {
        'messages': l,
        'start': start,
        'end': end,
    }

    return RETURN

def channel_leave(token, channel_id):
    valid_chid = False
    valid_auth = False
    is_owner = False
    channel_index = 0
    user_index = 0
    token_id = 0
    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('channels')[channel_index].get('owner_members'))):
        if data.get('channels')[channel_index].get('owner_members')[i].get('u_id') == token_id:
            is_owner = True
            break
    
    if is_owner:
        raise AccessError("You cannnot remove owner!")
    
    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            valid_auth = True
            user_index = i
            break
    
    if not valid_auth:
        raise AccessError("This user is not in the channel!")

    del data.get('channels')[channel_index].get('all_members')[user_index]

    return {

    }

def channel_join(token, channel_id):
    valid_chid = False
    public_ch = False
    global_owner = False
    channel_index = 0
    user_index = 0
    token_id = 0

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            channel_index = i
            valid_chid = True
            if data.get('channels')[i].get('is_public') == True:
                public_ch = True
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            raise InputError("You are already a member!")
    
    for i in range(len(data.get('users'))):
        if data.get('users')[i].get('u_id') == token_id:
            user_index = i
            if data.get('users')[i].get('permission_id') == 1:
                global_owner = True
            else:
                break
    
    if (not global_owner) and (not public_ch):
        raise AccessError("This is a private channel!")

    dic = {
        'u_id': data.get('users')[user_index]['u_id'],
        'name_first': data.get('users')[user_index]['name_first'],
        'name_last': data.get('users')[user_index]['name_last'],
    }
    
    data.get('channels')[channel_index].get('all_members').append(dic)

    if global_owner:
        data.get('channels')[channel_index].get('owner_members').append(dic)

    return {
    }

def channel_addowner(token, channel_id, u_id):
    valid_chid = False
    #valid_auth = False
    already_owner = False
    global_owner = False
    is_owner = False
    channel_index = 0
    user_index = 0
    already_member = False
    token_id = 0

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break 
    if not valid_chid:
        raise InputError("Invalid channel id!")

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('users'))):
        if data.get('users')[i].get('u_id') == token_id:
            if data.get('users')[i].get('permission_id') == 1:
                global_owner = True
            else:
                break
    for i in range(len(data.get('channels')[channel_index].get('owner_members'))):
        if data.get('channels')[channel_index].get('owner_members')[i].get('u_id') == token_id:
            is_owner = True
            break  
    if (not is_owner) and (not global_owner):
        raise AccessError("No permission to add owner!")

    for i in range(len(data.get('channels')[channel_index].get('owner_members'))):
        if data.get('channels')[channel_index].get('owner_members')[i].get('u_id') == u_id:
            user_index = i
            already_owner = True
            break
    if  already_owner:
        raise InputError("User is an owner, cannot be added!")

    for i in range(len(data.get('users'))):
        if data.get('users')[i].get('u_id') == u_id:
            user_index = i
            break
    
    dic = {
        'u_id': data.get('users')[user_index]['u_id'],
        'name_first': data.get('users')[user_index]['name_first'],
        'name_last': data.get('users')[user_index]['name_last'],
    }
    
    data.get('channels')[channel_index].get('owner_members').append(dic)
    
    for i in data.get('channels')[channel_index].get('all_members'):
        if i['u_id'] == u_id:
            already_member = True
            break
    
    if not already_member:
        data.get('channels')[channel_index].get('all_members').append(dic)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    valid_chid = False
    #valid_auth = False
    already_owner = False
    global_owner = False
    is_owner = False
    channel_index = 0
    user_index = 0
    token_id = 0

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break 
    if not valid_chid:
        raise InputError("Invalid channel id!")

    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']

    for i in range(len(data.get('users'))):
        if data.get('users')[i].get('u_id') == token_id:
            if data.get('users')[i].get('permission_id') == 1:
                global_owner = True
            else:
                break

    for i in range(len(data.get('channels')[channel_index].get('owner_members'))):
        if data.get('channels')[channel_index].get('owner_members')[i].get('u_id') == token_id:
            is_owner = True
            break  
    if (not is_owner) and (not global_owner):
        raise AccessError("No permission to remove owner!")

    for i in range(len(data.get('channels')[channel_index].get('owner_members'))):
        if data.get('channels')[channel_index].get('owner_members')[i].get('u_id') == u_id:
            already_owner = True
            user_index = i
            break
    if not already_owner:
        raise InputError("User's not an owner, cannot be removed!")

    del data.get('channels')[channel_index].get('owner_members')[user_index]

    return {
    }
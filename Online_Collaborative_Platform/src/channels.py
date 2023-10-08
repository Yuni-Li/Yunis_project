from channel_data import data
from error import InputError

def channels_list(token):
    # using the uid as the token
    channels = []
    # u_id of token
    token_id = 0
    for i in data['users']:
        if i['token'] == token:
            token_id = i['u_id']
            break

    for i in data['channels']:
        for j in i['all_members']:
            if j['u_id'] == token_id:
                res = {
                    'channel_id': i['channel_id'],
                    'name': i['name']
                }
                channels.append(res)
                break
    
    return {
        'channels': channels
    }
def channels_listall(token):
    channels = []
    for i in data['channels']:
        res = {
            'channel_id' : i['channel_id'],
            'name': i['name']
        }
        channels.append(res)
    return {
        'channels': channels
    }
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise InputError("Name should not be more than 20 characters long")
    channel_id = len(data['channels'])
    user = {}
    for i in data['users']:
        if i['token'] == token:
            user['u_id'] = i['u_id']
            user['name_first'] = i['name_first']
            user['name_last'] = i['name_last']
            break

    channel = {
        'channel_id': channel_id,
        'is_public': is_public,
        'name': name,
        'owner_members' : user,
        'all_member' : user,
        'messages': [],
    }
    data['channels'].append(channel)
    return {
        'channel_id': channel_id,
    }


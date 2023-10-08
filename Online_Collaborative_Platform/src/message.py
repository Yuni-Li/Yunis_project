from channel_data import data
from error import InputError, AccessError
from time import time

# this can be culculated what is the id of new message
total_mes_send = 0

def message_send(token, channel_id, message):
    global total_mes_send
    is_member = False
    if len(message) > 1000:
        raise InputError('Message cannot be more than 1000 characters')

    # the u_id of token
    u_id = 0
    for i in data['users']:
        if i['token'] == token:
            u_id = i['u_id']
            break
    
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
                    break

    if not is_member:
        raise AccessError('You are not a member of this channel')

    for i in data['channels']:
        if i['channel_id'] == channel_id:
            total_mes_send += 1
            dic = {}
            dic['message_id'] = total_mes_send
            dic['u_id'] = u_id
            dic['message'] = message
            dic['time_created'] = int(time())

            i['messages'].append(dic)

    return {
        'message_id': total_mes_send,
    }

def message_remove(token, message_id):
    valid_id = False
    is_owner = False
    global_owner = False
    # u_id of token
    u_id = 0
    # the u_id which send the messeage
    send_by_id = 0
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                send_by_id = j['u_id']
                valid_id = True
                break
    
    if not valid_id:
        raise InputError('Message no longer exists')

    for i in data['users']:
        if i['token'] == token:
            u_id = i['u_id']
            if i['permission_id'] == 1:
                global_owner = True
            break
    
    for i in data['channels']:
        for j in i['owner_members']:
            if j['u_id'] == u_id:
                is_owner = True
                break

    if is_owner or global_owner or u_id == send_by_id:
        for i in data['channels']:
            for j in i['messages']:
                if j['message_id'] == message_id:
                    i['messages'].remove(j)
    else:
        raise AccessError('You cannot remove this messages')


    return {
    }

def message_edit(token, message_id, message):
    is_owner = False
    global_owner = False
    # u_id of token
    u_id = 0
    # u_id which send message
    send_by_id = 0
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                send_by_id = j['u_id']
                break

    for i in data['users']:
        if i['token'] == token:
            u_id = i['u_id']
            if i['permission_id'] == 1:
                global_owner = True
            break
    
    for i in data['channels']:
        for j in i['owner_members']:
            if j['u_id'] == u_id:
                is_owner = True
                break

    if is_owner or global_owner or u_id == send_by_id:
        for i in data['channels']:
            for j in i['messages']:
                if j['message_id'] == message_id:
                    if len(message) == 0:
                        i['messages'].remove(j)
                    else:
                        j['message'] = message
    else:
        raise AccessError('You cannot remove this messages')

    return {
    }
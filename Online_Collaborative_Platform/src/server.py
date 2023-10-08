import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
from time import time, sleep
import jwt
from check import check_email, check_password, check_name
import hashlib
import pickle
import string
import random
import yagmail

# this is for decoding
SECRET = 'sempai'

# data for storing users and channels
data = {
    'users':[],
    'channels': [],
    'total_mes_send': 0,
    'standups': [],
}

try:
    data = pickle.load(open('data.p', 'rb'))
except Exception:
    pass

# this can be culculated what is the id of new message
total_mes_send = data['total_mes_send']

def save():
    global data
    data['total_mes_send'] = total_mes_send
    with open('data.p', 'wb') as FILE:
        pickle.dump(data, FILE)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register", methods=['POST'])
def register():
    global data
    args = request.get_json()
    email = str(args.get('email'))
    password = str(args.get('password'))
    name_first = str(args.get('name_first'))
    name_last = str(args.get('name_last'))

    # check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError(description="Invalid Email!")
        
    for new_user in data['users']:
        # check whether email is already exist
        if new_user['email'] == email:
            raise InputError(description="Email address is already being used by another user!")
            
    # check whether password is valid
    if check_password(password) == "Invalid Password":
        raise InputError(description="Password entered is less than 6 characters long!")
    
    elif check_name(name_first, name_last) == "Invalid First Name":
        # if the length of first name is not between 1-50 and contains numbers and symbols
        raise InputError(description="First name should between 1 and 50 characters!")
        
    elif check_name(name_first, name_last) == "Invalid Last Name":
        # if the length of last name is not between 1-50 and contains numbers and symbols
        raise InputError(description="Last name should between 1 and 50 characters!")

    concatentation = name_first[0].lower() + name_last.lower()

    # if concatentation is longer than 20, cutoff at 20
    if len(concatentation) > 20:
        concatentation = concatentation[:20]

    token = jwt.encode({'u_id': len(data['users'])}, SECRET, algorithm='HS256').decode()
    newUser = {}
    if len(data['users']) == 0:
        newUser = {
            'u_id': len(data['users']),
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'permission_id': 1,
            'token': token,
            'handle_str': concatentation,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'profile_img_url': '',
        }
    else:
        newUser = {
            'u_id': len(data['users']),
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'permission_id': 2,
            'token': token,
            'handle_str': concatentation,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'profile_img_url': '',
        }
    
    # add new user to 'data'
    data['users'].append(newUser)

    save()

    return dumps({
        'u_id': newUser['u_id'],
        'token': token,
    })

@APP.route("/auth/login", methods=['POST'])
def login():
    global data
    args = request.get_json()
    email = str(args.get('email'))
    password = str(args.get('password'))

    # check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError("Email entered is not a valid")
    
    # set exist_email as false, that is email does not belong to a user
    exist_email = False    
    u_id = 0
    for user in data['users']:
        if email == user['email']:
            # if email is already exist, set exist_email as true
            exist_email = True

            # check if password is correct
            password = hashlib.sha256(password.encode()).hexdigest()
            if password != user['password']:
                raise InputError("Incorrect Password!")
            
            u_id = user['u_id']
            user['token'] = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256').decode()
            break
        
    # if email is not in 'data'
    if exist_email is not True:
        raise InputError("Email entered does not belong to a user!")
    
    save()

    return {
        'u_id': u_id,
        'token': jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256').decode(),
    }

@APP.route("/auth/logout", methods=['POST'])
def logout():
    global data
    args = request.get_json()
    token = str(args.get('token'))

    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    is_success = False
    for user in data['users']:
        if user['u_id'] == u_id:
            user['token'] = ''
            is_success = True
            break

    save()

    return dumps({'is_success': is_success})

@APP.route("/auth/passwordreset/request", methods=['POST'])
def setrequest():
    global data
    args = request.get_json()
    email = str(args.get('email'))

    valid_mail = False

    for user in data['users']:
        if user['email'] == email:
            valid_mail = True
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7)))
            user['reset_code'] = result_str
            break
    
    if not valid_mail:
        raise InputError(description='Email does not exist')

    yag = yagmail.SMTP('410446@gm.tnfsh.tn.edu.tw', 'szscvidbnrarmsxe')

    yag.send(to=email, subject='test', contents=result_str)

    save()

    return dumps({})

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def reset():
    global data
    args = request.get_json()
    new_password = str(args.get('new_password'))
    reset_code = str(args.get('reset_code'))

    for user in data['users']:
        if user['reset_code'] == reset_code:
            user['reset_code'] = ''
            if check_password(new_password) == "Invalid Password":
                raise InputError(description="Password entered is less than 6 characters long!")
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            break

    save()

    return dumps({})

############## channels.py --- list ##############
@APP.route('/channels/list', methods=['GET'])
def server_channels_list():
    global data
    
    # using the uid as the token
    channels = []
    token = str(request.args.get('token'))
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in data['channels']:
        for j in i['all_members']:
            if j['u_id'] == token_id:
                res = {
                    'channel_id': i['channel_id'],
                    'name': i['name']
                }
                channels.append(res)

    return dumps({
        'channels': channels
    })

############# channels.py --- listall #############
@APP.route('/channels/listall', methods=['GET'])
def server_channels_listall():
    global data
    channels = []
    for i in data['channels']:
        res = {
            'channel_id' : i['channel_id'],
            'name': i['name']
        }
        channels.append(res)
    return dumps({
        'channels': channels
    })

############# channels.py --- create #############
@APP.route('/channels/create', methods=['POST'])
def server_channels_create():
    global data
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = bool(payload['is_public'])
    
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    if len(name) > 20:
        raise InputError(description="Name should not be more than 20 characters long")
    channel_id = len(data['channels'])
    user = {}
    owner = []
    member = []
    for i in data['users']:
        if i['u_id'] == token_id:
            user['u_id'] = token_id
            user['name_first'] = i['name_first']
            user['name_last'] = i['name_last']
            owner.append(user)
            member.append(user)
            break

    channel = {
        'channel_id': channel_id,
        'is_public': is_public,
        'name': name,
        'owner_members' : owner,
        'all_members' : member,
        'messages': [],
    }
    data['channels'].append(channel)

    save()

    return dumps({
        'channel_id': channel_id,
    })

@APP.route("/channel/invite", methods=['POST'])
def invite():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    u_id = int(args.get('u_id'))
    
    valid_uid = False
    valid_chid = False
    valid_auth = False  # check if authorised user is in channel
    already_member = False
    channel_index = 0
    user_index = 0
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
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
        raise InputError(description='Input invalid user id or channel id!')
    
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['all_members']:
                if j['u_id'] == token_id:
                    valid_auth = True
                    break
    
    if (not valid_auth):
        raise AccessError(description='Unable to invite!')

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

    save()

    return dumps({})

@APP.route("/channel/details", methods=['GET'])
def details():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))

    valid_chid = False
    valid_auth = False  # check if authorised user is in channel
    channel_index = 0
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError('Invalid channel id!')

    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['all_members']:
                if j['u_id'] == token_id:
                    valid_auth = True
                    break
    
    if not valid_auth:
        raise AccessError('You are not a member of this channel!')

    name = data.get('channels')[channel_index].get('name')
    owner = data.get('channels')[channel_index].get('owner_members')
    member = data.get('channels')[channel_index].get('all_members')

    L = {'name': name, 'owner_members': owner, 'all_members': member,}
    return dumps(L) 

@APP.route("/channel/messages", methods=['GET'])
def messages():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    valid_chid = False
    valid_auth = False
    channel_index = 0
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")

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
        dic = data.get('channels')[channel_index].get('messages')[i].copy()
        for reacts in dic['reacts']:
            if token_id in reacts['u_ids']:
                reacts['is_this_user_reacted'] = True
            else:
                reacts['is_this_user_reacted'] = False
        l = [dic] + l
    
    if start + 50 > len(data.get('channels')[channel_index].get('messages')):
        end = -1
    
    RETURN = {
        'messages': l,
        'start': start,
        'end': end,
    }

    return dumps(RETURN)

@APP.route("/channel/leave", methods=['POST'])
def leave():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))

    valid_chid = False
    valid_auth = False
    channel_index = 0
    user_index = 0
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")
    
    for i in range(len(data.get('channels')[channel_index].get('all_members'))):
        if data.get('channels')[channel_index].get('all_members')[i].get('u_id') == token_id:
            valid_auth = True
            user_index = i
            break
    
    if not valid_auth:
        raise AccessError("This user is not in the channel!")

    del data.get('channels')[channel_index].get('all_members')[user_index]

    save()

    return dumps({})

@APP.route("/channel/join", methods=['POST'])
def join():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))

    valid_chid = False
    public_ch = False
    global_owner = False
    channel_index = 0
    user_index = 0
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            channel_index = i
            valid_chid = True
            if data.get('channels')[i].get('is_public') == True:
                public_ch = True
            break
    
    if not valid_chid:
        raise InputError("Invalid channel id!")

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

    # global owner will also become owner of that channel
    if global_owner:
        data.get('channels')[channel_index].get('owner_members').append(dic)

    save()

    return dumps({})

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    u_id = int(args.get('u_id'))

    valid_chid = False
    already_owner = False
    global_owner = False
    is_owner = False
    channel_index = 0
    user_index = 0
    already_member = False
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break 
    if not valid_chid:
        raise InputError("Invalid channel id!")

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

    save()

    return dumps({})

@APP.route("/channel/removeowner", methods=['POST'])
def remove():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    u_id = int(args.get('u_id'))

    valid_chid = False
    already_owner = False
    global_owner = False
    is_owner = False
    channel_index = 0
    user_index = 0
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    for i in range(len(data.get('channels'))):
        if data.get('channels')[i].get('channel_id') == channel_id:
            valid_chid = True
            channel_index = i
            break 
    if not valid_chid:
        raise InputError("Invalid channel id!")

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

    save()

    return dumps({})

@APP.route("/message/send", methods = ['POST'])
def send():
    global total_mes_send
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    message = str(args.get('message'))

    is_member = False
    if len(message) > 1000:
        raise InputError(description='Message cannot be more than 1000 characters')

    # the u_id of token
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
                    break

    if not is_member:
        raise AccessError(description='You are not a member of this channel')

    for i in data['channels']:
        if i['channel_id'] == channel_id:
            total_mes_send += 1
            dic = {}
            dic['message_id'] = total_mes_send
            dic['u_id'] = u_id
            dic['message'] = message
            dic['time_created'] = int(time())
            dic['reacts'] = [
                {
                    'react_id': 1,
                    'u_ids':[],
                }
            ]
            dic['is_pinned'] = False

            i['messages'].append(dic)

    save()

    return dumps({
        'message_id': total_mes_send,
    })

@APP.route("/message/remove", methods=['DELETE'])
def m_remove():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))

    valid_id = False
    is_owner = False
    global_owner = False
    # u_id of token
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    # the u_id which send the messeage
    send_by_id = 0
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                send_by_id = j['u_id']
                valid_id = True
                break
    
    if not valid_id:
        raise InputError(description='Message no longer exists')

    for i in data['users']:
        if u_id == i['u_id']:
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
        raise AccessError(description='You cannot remove this messages')

    save()

    return dumps({})

@APP.route("/message/edit", methods=['PUT'])
def edit():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))
    message = str(args.get('message'))

    is_owner = False
    global_owner = False
    # u_id of token
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    # u_id which send message
    send_by_id = 0
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                send_by_id = j['u_id']
                break

    for i in data['users']:
        if u_id == i['u_id']:
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
        raise AccessError(description='You cannot edit this messages')

    save()

    return dumps({})

@APP.route("/message/sendlater", methods = ['POST'])
def sendlater():
    global total_mes_send
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    message = str(args.get('message'))
    time_sent = int(args.get('time_sent'))

    
    
    is_member = False
    valid_chid = False
    if len(message) > 1000:
        raise InputError(description='Message cannot be more than 1000 characters')

    # the u_id of token
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            valid_chid = True
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
                    break

    if not valid_chid:
        raise InputError(description='Invalid channel id')

    if not is_member:
        raise AccessError(description='You are not a member of this channel')

    if time_sent < int(time()):
        raise InputError(description='Time sent is a time in the past')

    sleep(time_sent - int(time()))

    for i in data['channels']:
        if i['channel_id'] == channel_id:
            total_mes_send += 1
            dic = {}
            dic['message_id'] = total_mes_send
            dic['u_id'] = u_id
            dic['message'] = message
            dic['time_created'] = time_sent
            dic['reacts'] = [
                {
                    'react_id': 1,
                    'u_ids':[],
                }
            ]
            dic['is_pinned'] = False

            i['messages'].append(dic)

    save()

    return dumps({
        'message_id': total_mes_send,
    })
    

@APP.route("/message/react", methods = ['POST'])
def react():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))
    react_id = int(args.get('react_id'))

    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    valid_message_id = False
    react_exist = False

    if react_id != 1:
        raise InputError(description='Invalid react id')

    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                for user in i['all_members']:
                    if user['u_id'] == token_id:
                        valid_message_id = True
                        for reacts in j['reacts']:
                            if react_id == reacts['react_id']:
                                react_exist = True
                                if token_id not in reacts['u_ids']:
                                    reacts['u_ids'].append(token_id)
                                else:
                                    raise InputError(description='This message has been reacted')
                                break
    
    if not react_exist:
        for i in data['channels']:
            for j in i['messages']:
                if message_id == j['message_id']:
                    dic = {
                        'reacts_id': react_id,
                        'u_ids': [token_id],
                    }
                    j['reacts'].append(dic)
    
    if not valid_message_id:
        raise InputError(description='Message_id is not valid within a channel that you have joined')


    save()

    return dumps({})

@APP.route("/message/unreact", methods = ['POST'])
def unreact():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))
    react_id = int(args.get('react_id'))

    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    valid_message_id = False

    if react_id != 1:
        raise InputError(description='Invalid react id')

    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                for user in i['all_members']:
                    if user['u_id'] == token_id:
                        valid_message_id = True
                        for reacts in j['reacts']:
                            if react_id == reacts['react_id']:
                                if token_id in reacts['u_ids']:
                                    reacts['u_ids'].remove(token_id)
                                else:
                                    raise InputError(description='This message has not been reacted')
    
    if not valid_message_id:
        raise InputError(description='Message_id is not valid within a channel that you have joined')


    save()

    return dumps({})

@APP.route("/message/pin", methods = ['POST'])
def pin():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))

    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    valid_message_id = False
    is_owner = False
    global_owner = False
    is_member = False

    for i in data['users']:
        if i['u_id'] == token_id:
            if i['permission_id'] == 1:
                global_owner = True
                break
    
    channel_id = 0
    
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                valid_message_id = True
                channel_id = i['channel_id']
                for user in i['owner_members']:
                    if user['u_id'] == token_id:
                        is_owner = True
                        is_member = True
                        break
                break

    if not valid_message_id:
        raise InputError(description='Invalid message id')

    if (not global_owner) and (not is_member) and (not is_owner):
        raise AccessError(description='You are not authorised to pin message')


    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['messages']:
                if j['message_id'] == message_id:
                    if not j['is_pinned']:
                        j['is_pinned'] = True
                    else:
                        raise InputError(description='Message is already pinned')
    
    save()

    return dumps({})

@APP.route("/message/unpin", methods = ['POST'])
def unpin():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    message_id = int(args.get('message_id'))

    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])

    valid_message_id = False
    is_owner = False
    global_owner = False
    is_member = False

    for i in data['users']:
        if i['u_id'] == token_id:
            if i['permission_id'] == 1:
                global_owner = True
                break
    
    channel_id = 0
    
    for i in data['channels']:
        for j in i['messages']:
            if j['message_id'] == message_id:
                valid_message_id = True
                channel_id = i['channel_id']
                for user in i['owner_members']:
                    if user['u_id'] == token_id:
                        is_owner = True
                        is_member = True
                        break
                break

    if not valid_message_id:
        raise InputError(description='Invalid message id')

    if (not global_owner) and (not is_member) and (not is_owner):
        raise AccessError(description='You are not authorised to unpin message')


    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for j in i['messages']:
                if j['message_id'] == message_id:
                    if j['is_pinned']:
                        j['is_pinned'] = False
                    else:
                        raise InputError(description='Message is already unpinned')
    
    save()

    return dumps({})
                        
@APP.route("/users/all", methods=['GET'])
def users_all():
    users = []
    for i in data['users']:
        dic = {}
        dic['u_id'] = i['u_id']
        dic['email'] = i['email']
        dic['name_first'] = i['name_first']
        dic['name_last'] = i['name_last']
        dic['handle_str'] = i['handle_str']
        dic['profile_img_url'] = i['profile_img_url']
        users.append(dic)
    return dumps({
        'users': users
    })

@APP.route("/admin/userpermission/change", methods=['POST'])
def permission_change():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    u_id = int(args.get('u_id'))
    permission_id = int(args.get('permission_id'))

    valid_uid = False
    is_owner = False
    # u_id of token
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    for i in data['users']:
        if i['u_id'] == u_id:
            valid_uid = True
            break
    
    if not valid_uid:
        raise InputError('Invalid user id')

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

    save()
    
    return dumps({})

@APP.route("/search", methods=['GET'])
def search():
    token = str(request.args.get('token'))
    query_str = str(request.args.get('query_str'))

    l = []
    token_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    for i in data['channels']:
        for j in i['messages']:
            if (j['u_id'] == token_id) and (query_str in j['message']):
                dic = j.copy()
                for reacts in dic['reacts']:
                    if token_id in reacts['u_ids']:
                        reacts['is_this_user_reacted'] = True
                    else:
                        reacts['is_this_user_reacted'] = False
                l.append(dic)

    return dumps({
        'messages': l
    })

@APP.route("/user/profile", methods=['GET'])
def user_profile():
    u_id = int(request.args.get('u_id'))

    target_profile = {}
    for i in data['users']:
        if i['u_id'] == u_id:
            target_profile['u_id'] = i['u_id']
            target_profile['email'] = i['email']
            target_profile['name_first'] = i['name_first']
            target_profile['name_last'] = i['name_last']
            target_profile['handle_str'] = i['handle_str']
            target_profile['profile_img_url'] = i['profile_img_url']
            break
    if target_profile == {}:
        raise InputError('This is not a valid user')

    return dumps({'user': target_profile})

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    name_first = str(args.get('name_first'))
    name_last = str(args.get('name_last'))
    
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('first name exceeds the length limit')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('last name exceeds the length limit')
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    for i in data['users']:
        if i['u_id'] == u_id:
            i['name_first'] = name_first
            i['name_last'] = name_last
            break

    for i in data['channels']:
        for owner in i['owner_members']:
            if owner['u_id'] == u_id:
                owner['name_first'] = name_first
                owner['name_last'] = name_last
                break
        for member in i['all_members']:
            if member['u_id'] == u_id:
                member['name_first'] = name_first
                member['name_last'] = name_last
                break
    
    save()

    return dumps({})

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    email = str(args.get('email'))

    exist_email = False

    # check whether email is valid
    if check_email(email) == "Invalid Email":
        raise InputError(description="Invalid Email!")

    for i in data['users']:
        if i['email'] == email:
            exist_email = True
            break
    if exist_email:
        raise InputError('Email address already exists')
    
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    for i in data['users']:
        if i['u_id'] == u_id:
            i['email'] = email

    save()

    return dumps({})

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    handle_str = str(args.get('handle_str'))

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError('str length must be between 3 - 20')

    for i in data['users']:
        if i['handle_str'] == handle_str:
            raise InputError('Handle already exists')

    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    for i in data['users']:
        if i['u_id'] == u_id:
            i['handle_str'] = handle_str
            break

    save()

    return dumps({})


@APP.route("/clear", methods=['DELETE'])
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

    save()

    return dumps({})    


@APP.route("/standup/start", methods=['POST'])
def standup_start():
    global data
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    length = int(args.get('length'))
    
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    is_member = False
    valid_chid = False
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            valid_chid = True
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
            break
    if (not valid_chid) or (not is_member):
        raise InputError('Invalid channel id')
        
    time_finish = int(time()) + length
    
    save()
    
    return dumps({
        'time_finish': time_finish,
    })


@APP.route("/standup/active", methods=['GET'])
def standup_active():
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    is_member = False
    valid_chid = False
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            valid_chid = True
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
            break
    if (not valid_chid) or (not is_member):
        raise InputError('Invalid channel id')
    
    return dumps({
        'is_active': True,
        'time_finish': 123,
    })
    

@APP.route("/standup/send", methods=['POST'])
def standup_send():
    global data
    global total_mes_send
    args = request.get_json()
    token = str(args.get('token'))
    channel_id = int(args.get('channel_id'))
    message = str(args.get('message'))

    if len(message) > 1000:
        raise InputError('Message cannot be more than 1000 characters')

    valid_chid = False
    is_member = False
    u_id = int(jwt.decode(token, SECRET, algorithm=['HS256'])['u_id'])
    
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            valid_chid = True
            for j in i['all_members']:
                if j['u_id'] == u_id:
                    is_member = True
                    break

    if not valid_chid:
        raise InputError('Invalid channel id')
    if not is_member:
        raise AccessError('You are not a member of this channel')

    save()

    return dumps({})


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

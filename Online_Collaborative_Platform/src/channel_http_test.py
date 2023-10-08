# this will test channel.py, message.py, and other.py

import pytest
from error import InputError, AccessError
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import urllib

# token with u_id
token_0 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowfQ.F5mHVvY1jyS0zrs7sxx6n1aplord-UW_3Mr4vjfUUk0'
token_1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxfQ.ZrE0yQnKGh70FBqztJEr-2nTS_kP1BrsXH-5SMXB1Uw'
token_2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoyfQ.srPNNrhtrEr89PmhIUwxUEtS9YrXvmOYgyw8MAB_wEs'
token_3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjozfQ.WfTjcMa-duEPS_LUnCTA3mu94_gZRroCSsEMS2mhkcI'

# This fixture gets the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_users_all(url):
    requests.delete(url+'clear')
    requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'SUPER',
        'name_last': 'USER',
    })
    requests.post(url + 'auth/register', json = {
        'email': 'user1@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
    })
    requests.post(url + 'auth/register', json = {
        'email': 'user2@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Kusuo',
        'name_last': 'Saiki',
    })
    requests.post(url + 'auth/register', json = {
        'email': 'user3@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Kokomi',
        'name_last': 'Teruhashi',
    })
    queryString = urllib.parse.urlencode({
        'token': token_1,
    })
    resp = requests.get(url + 'users/all?' + queryString)
    
    assert resp.status_code == 200

def test_admin_userpermission_change(url):
    # not global owner
    r = requests.post(url + 'admin/userpermission/change', json = {'token': token_1, 'u_id': 2, 'permission_id': 1})
    assert r.status_code == 400

    requests.post(url + 'admin/userpermission/change', json = {'token': token_0, 'u_id': 1, 'permission_id': 1})

    requests.post(url + 'admin/userpermission/change', json = {'token': token_0, 'u_id': 1, 'permission_id': 2})

def test_channel_invite(url):
    r = requests.post(url + '/channels/create', json = {'token': token_1, 'name': 'Hayden', 'is_public': False})
    assert r.status_code == 200
    r = requests.post(url + '/channels/create', json = {'token': token_2, 'name': 'channel2', 'is_public': True})
    assert r.status_code == 200

    requests.post(url + '/channel/invite', json = {'token': token_2, 'channel_id': 1, 'u_id': 3})
    # invalid channel
    r = requests.post(url + 'channel/invite', json = {'token': token_0, 'channel_id': 3, 'u_id': 3})
    assert r.status_code == 400
    
    # invalid_user
    r = requests.post(url + 'channel/invite', json = {'token': token_1, 'channel_id': 0, 'u_id': 4})
    assert r.status_code == 400

    # not_member
    r = requests.post(url + 'channel/invite', json = {'token': token_2, 'channel_id': 0, 'u_id': 3})
    assert r.status_code == 400

    # already_member
    r = requests.post(url + 'channel/invite', json = {'token': token_1, 'channel_id': 0, 'u_id': 1})
    assert r.status_code == 400

def test_channel_details(url):
    requests.post(url + '/channel/invite', json = {'token': token_1, 'channel_id': 0, 'u_id': 2})

    # invalid_ch
    queryString = urllib.parse.urlencode({
        'token': token_1,
        'channel_id': 3
    })
    r = requests.get(url + '/channel/details?' + queryString)
    assert r.status_code == 400

    # not_member
    queryString = urllib.parse.urlencode({
        'token': token_3,
        'channel_id': 0
    })
    r = requests.get(url + '/channel/details?' + queryString)
    assert r.status_code == 400

def test_message_send(url):
    # not a member
    r = requests.post(url + '/message/send', json = {'token': token_1, 'channel_id': 2, 'message': 'Hello World'})
    assert r.status_code == 400

def test_channel_messages(url):
    requests.post(url + '/message/send', json = {'token': token_1, 'channel_id': 0, 'message': 'Hello World'})
    requests.post(url + '/message/send', json = {'token': token_2, 'channel_id': 1, 'message': 'Hello'})

    # invalid channel
    queryString = urllib.parse.urlencode({
        'token': token_1,
        'channel_id': 2,
        'start': 0
    })
    r = requests.get(url + '/channel/messages?' + queryString)
    assert r.status_code == 400
    
    # invalid start
    queryString = urllib.parse.urlencode({
        'token': token_1,
        'channel_id': 1,
        'start': 49
    })
    r = requests.get(url + '/channel/messages?' + queryString)
    assert r.status_code == 400
    
    # invalid user
    queryString = urllib.parse.urlencode({
        'token': token_3,
        'channel_id': 0,
        'start': 0
    })
    r = requests.get(url + '/channel/messages?' + queryString)
    assert r.status_code == 400

def test_search(url):
    queryString = urllib.parse.urlencode({
        'token': token_2,
        'query_str': 'Hello',
    }) 
    resp = requests.get(url + '/search?' + queryString)
    assert resp.status_code == 200

def test_message_edit_remove(url):
    requests.put(url + '/message/edit', json = {'token': token_1, 'message_id': 1, 'message': ''}) 

    # Message with message_id was not sent by the authorised user making this request
    r = requests.delete(url + '/message/remove', json = {'token': token_3, 'message_id': 2}) 
    assert r.status_code == 400

    requests.delete(url + '/message/remove', json = {'token': token_2, 'message_id': 2})

    # Message no longer exists
    r = requests.delete(url + '/message/remove', json = {'token': token_2, 'message_id': 2})
    assert r.status_code == 400

def test_channel_leave(url):
    requests.post(url+'/channel/invite', json = {'token': token_1, 'channel_id': 0, 'u_id': 2})
    requests.post(url+'/channel/leave', json = {'token': token_2, 'channel_id': 0})
    
    # invalid channel
    r = requests.post(url+'/channel/leave', json = {'token': token_1, 'channel_id': 2})
    assert r.status_code == 400
    
    # invalid user
    r = requests.post(url+'/channel/leave', json = {'token': token_2, 'channel_id': 0})
    assert r.status_code == 400

def test_channel_join(url):
    requests.post(url+'/channel/join', json = {'token': token_1, 'channel_id': 1})
    requests.post(url+'/channel/join', json = {'token': '0', 'channel_id': 0})

    # invalid channel
    r = requests.post(url+'/channel/join', json = {'token': token_1, 'channel_id': 2})
    assert r.status_code == 400

    # private channel
    r = requests.post(url+'/channel/join', json = {'token': token_3, 'channel_id': 0})
    assert r.status_code == 400

def test_channel_addowner(url):
    # invalid channel
    r = requests.post(url+'/channel/addowner', json = {'token': token_1, 'channel_id': 2, 'u_id': 2})
    assert r.status_code == 400

    requests.post(url+'/channel/addowner', json = {'token': token_1, 'channel_id': 0, 'u_id': 0})

    # user is already an owner in the channel
    r = requests.post(url+'/channel/addowner', json = {'token': token_1, 'channel_id': 0, 'u_id': 0})
    assert r.status_code == 400

    # invalid auth
    r = requests.post(url+'/channel/addowner', json = {'token': token_3, 'channel_id': 1, 'u_id': 1})
    assert r.status_code == 400

    r = requests.post(url+'/channel/addowner', json = {'token': token_2, 'channel_id': 1, 'u_id': 1})
    r.status_code == 200

def test_channel_removeowner(url):
    requests.post(url+'/channel/addowner', json = {'token': token_1, 'channel_id': 0, 'u_id': 0})
    r = requests.post(url+'/channel/removeowner', json = {'token': token_1, 'channel_id': 0, 'u_id': 0})
    r.status_code == 200
    
    # invalid channel
    r = requests.post(url+'/channel/removeowner', json = {'token': token_1, 'channel_id': 3, 'u_id': 2})
    assert r.status_code == 400

    # invalid user
    r = requests.post(url+'/channel/removeowner', json = {'token': token_2, 'channel_id': 1, 'u_id': 3})
    assert r.status_code == 400

    # invalid user
    r = requests.post(url+'/channel/removeowner', json = {'token': token_3, 'channel_id': 1, 'u_id': 2})
    assert r.status_code == 400
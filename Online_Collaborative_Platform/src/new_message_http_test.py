import pytest
import re
from error import InputError, AccessError
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
import json
import urllib

# token with u_id
token_0 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowfQ.F5mHVvY1jyS0zrs7sxx6n1aplord-UW_3Mr4vjfUUk0'
token_1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxfQ.ZrE0yQnKGh70FBqztJEr-2nTS_kP1BrsXH-5SMXB1Uw'
token_2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoyfQ.srPNNrhtrEr89PmhIUwxUEtS9YrXvmOYgyw8MAB_wEs'

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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

def test_sendlater(url):
    requests.delete(url+'clear')
    requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
    })
    requests.post(url + 'auth/register', json = {
        'email': 'user1@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Gawr',
        'name_last': 'Gura',
    })
    requests.post(url + 'auth/register', json = {
        'email': 'user2@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Watson',
        'name_last': 'Amelia',
    })
    requests.post(url + '/channels/create', json = {'token': token_0, 'name': 'EVA', 'is_public': False})
    requests.post(url + '/channel/invite', json = {'token': token_0, 'channel_id': 0, 'u_id': 1})

    requests.post(url + '/channels/create', json = {'token': token_2, 'name': 'EVA2', 'is_public': False})
    requests.post(url + 'message/send', json = {
        'token': token_2,
        'channel_id': 1,
        'message': 'Hello!!!',
    })


    requests.post(url + 'message/sendlater', json = {
        'token': token_0,
        'channel_id': 0,
        'message': 'Hello!!!',
        'time_sent': int(time()) + 2,
    })

    sleep(5)

    queryString = urllib.parse.urlencode({
        'token': token_0,
        'channel_id': 0,
        'start': 0,
    })

    resp = requests.get(url + 'channel/messages?' + queryString)
    
    assert len(json.loads(resp.text)['messages']) == 1

    # invalid channel_id
    r = requests.post(url + 'message/sendlater', json = {
        'token': token_0,
        'channel_id': 2,
        'message': 'Hello!!!',
        'time_sent': int(time()) + 5,
    })
    assert r.status_code == 400

    # >1000 characters
    r = requests.post(url + 'message/sendlater', json = {
        'token': token_0,
        'channel_id': 0,
        'message': 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
        'time_sent': int(time()) + 5,
    })
    assert r.status_code == 400

    # time sent is a time in the past
    r = requests.post(url + 'message/sendlater', json = {
        'token': token_0,
        'channel_id': 0,
        'message': 'Hello!!!',
        'time_sent': int(time()) - 5,
    })
    assert r.status_code == 400

    # not in the channel
    r = requests.post(url + 'message/sendlater', json = {
        'token': token_2,
        'channel_id': 0,
        'message': 'Hello!!!',
        'time_sent': int(time()) + 5,
    })
    assert r.status_code == 400

def test_react_unreact(url):
    r = requests.post(url + 'message/react', json = {
        'token': token_0,
        'message_id': 1,
        'react_id': 1,
    })

    r = requests.post(url + 'message/react', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 1,
    })

    # not a valid message
    r = requests.post(url + 'message/react', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 1,
    })
    assert r.status_code == 400

    # invalid react id
    r = requests.post(url + 'message/react', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 2,
    })
    assert r.status_code == 400

    # already reacted
    r = requests.post(url + 'message/react', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 1,
    })
    assert r.status_code == 400

    requests.post(url + 'message/unreact', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 1,
    })

    # invalid message id
    r = requests.post(url + 'message/unreact', json = {
        'token': token_0,
        'message_id': 2,
        'react_id': 1,
    })
    assert r.status_code == 400

    # invalid react id
    r = requests.post(url + 'message/unreact', json = {
        'token': token_0,
        'message_id': 1,
        'react_id': 2,
    })
    assert r.status_code == 400

    # haven't reacted
    r = requests.post(url + 'message/unreact', json = {
        'token': token_1,
        'message_id': 1,
        'react_id': 1,
    })
    assert r.status_code == 400

def test_pin_unpin(url):
    r = requests.post(url + 'message/pin', json = {
        'token': token_0,
        'message_id': 1,
    })

    # invalid message id
    r = requests.post(url + 'message/pin', json = {
        'token': token_1,
        'message_id': 2,
    })
    assert r.status_code == 400

    # is pinneed
    r = requests.post(url + 'message/pin', json = {
        'token': token_1,
        'message_id': 1,
    })
    assert r.status_code == 400

    # not a member
    r = requests.post(url + 'message/pin', json = {
        'token': token_2,
        'message_id': 1,
    })
    assert r.status_code == 400

    # invalid message id
    r = requests.post(url + 'message/unpin', json = {
        'token': token_0,
        'message_id': 2,
    })
    assert r.status_code == 400

    # alredy unpinned
    r = requests.post(url + 'message/unpin', json = {
        'token': token_2,
        'message_id': 2,
    })
    assert r.status_code == 400

    # not a member or owner
    r = requests.post(url + 'message/unpin', json = {
        'token': token_1,
        'message_id': 2,
    })
    assert r.status_code == 400

    r = requests.post(url + 'message/unpin', json = {
        'token': token_0,
        'message_id': 1,
    })
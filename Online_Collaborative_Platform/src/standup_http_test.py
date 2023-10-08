import pytest
import re
from error import InputError, AccessError
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
import json

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

def test_standup_start(url):
    requests.delete(url+'clear')
    requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
    })
    requests.post(url + '/channels/create', json = {'token': token_0, 'name': 'EVA', 'is_public': True})
    r = requests.post(url + '/standup/start', json = {
        'token': token_0,
        'channel_id': 0,
        'length': 12,
    })
    assert r.status_code == 200

    r = requests.post(url + '/standup/start', json = {
        'token': token_0,
        'channel_id': 1,
        'length': '12',
    })
    assert r.status_code == 400  # Invalid channel id


def test_standup_active(url):
    requests.delete(url+'clear')
    requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
    })
    requests.post(url + '/channels/create', json = {'token': token_0, 'name': 'EVA', 'is_public': False})
    requests.post(url + '/standup/start', json = {
        'token': token_0,
        'channel_id': 0,
        'length': 123,
    })
    r = requests.get(url + '/standup/active', json = {
        'token': token_0,
        'channel_id': 0,
    })
    assert r.status_code == 200

    r = requests.get(url + '/standup/active', json = {
        'token': token_0,
        'channel_id': 1,
    })
    assert r.status_code == 400  # Invalid channel id
    
    
def test_standup_send(url):
    requests.delete(url+'clear')
    requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
    })
    requests.post(url + '/channels/create', json = {'token': token_0, 'name': 'EVA', 'is_public': False})
    requests.post(url + '/standup/start', json = {
        'token': token_0,
        'channel_id': 0,
        'length': 123,
    })
    r = requests.post(url + 'standup/send', json = {
        'token': token_0,
        'channel_id': 0,
        'message': 'Hello!!!',
    })
    assert r.status_code == 200
    
    r = requests.post(url + 'standup/send', json = {
        'token': token_0,
        'channel_id': 1,
        'message': 'Hello!!!',
    })
    assert r.status_code == 400  # invalid channel_id

    r = requests.post(url + 'standup/send', json = {
        'token': token_0,
        'channel_id': 0,
        'message': 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
    })
    assert r.status_code == 400  # >1000 characters
    
    r = requests.post(url + 'standup/send', json = {
        'token': token_2,
        'channel_id': 0,
        'message': 'Hello!!!',
    })
    assert r.status_code == 400  # not in the channel    


# this will test channels.py

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



########################################################################
# Test -> list of all users and their associated details
def test_channels_list(url):
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


    # Create channel-0 
    requests.post(url + 'channels/create', json = {'token': token_0, 'name': 'channel0','is_public': True})

    queryString = urllib.parse.urlencode({
        'token': token_0,
    })
    # valid channel0 as Test One
    resp = requests.get(url + '/channels/list?' + queryString)
    
    assert json.loads(resp.text) == {
        'channels': [
            {
                'channel_id': 0,
                'name' : "channel0",
            }
        ]
    }
    
    # Create channel-1
    requests.post(url + 'channels/create', json = {'token': token_1, 'name': 'channel1','is_public': False})

    queryString = urllib.parse.urlencode({
        'token': token_0,
    })
    # valid channel1 as Test Two
    resp = requests.get(url + '/channels/list?' + queryString)
    
    assert json.loads(resp.text) == {
        'channels': [
            {
                'channel_id': 0,
                'name' : "channel0",
            }
        ]
    }

########################################################################
def test_channels_listall(url):
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


    # Create channel-0-1-2
    requests.post(url + 'channels/create', json = {'token': token_0, 'name': 'channel0','is_public': True})
    requests.post(url + 'channels/create', json = {'token': token_1, 'name': 'channel1','is_public': True})
    requests.post(url + 'channels/create', json = {'token': token_2, 'name': 'channel2','is_public': True})
    queryString = urllib.parse.urlencode({
        'token': token_0,
    })

    resp = requests.get(url + '/channels/listall?' + queryString)
    
    assert json.loads(resp.text) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel0'
            },
            {
                'channel_id': 1,
                'name': 'channel1'
            },
            {
                'channel_id': 2,
                'name': 'channel2'     
            },
        ]
    }

########################################################################
def test_channels_create(url):
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


    # Create channel-0 with length > 20 
    r = requests.post(url + 'channels/create', json = {'token': token_0, 'name': 'This_Channels_Name_Is_Longer_Than_20','is_public': True})
    assert r.status_code == 400

    # Create channel-1 with length < 20
    r = requests.post(url + 'channels/create', json = {'token': token_1, 'name': 'channel1','is_public': True})
    assert r.status_code == 200

    # Create channel-1 with length = 20
    r = requests.post(url + 'channels/create', json = {'token': token_1, 'name': 'channel1901234567890','is_public': True})
    assert r.status_code == 200

########################################################################





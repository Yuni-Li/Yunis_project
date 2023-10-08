import pytest
from error import InputError, AccessError
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import urllib
#import server

# token with u_id
token0 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMCJ9.wy3AHypqq_AIkiowwNO_kgpC27AVblEAsEiC-PS8ssw'
token1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMSJ9.tG5Hn2s1TlzfEGwciSACol5VcRDJkaU-1M6GOP96IoA'
token2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMiJ9.zUZPbfJzZYvhmGEAImHSUJGHDx_VxIAooSYpn4PJAtE'
token3 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMyJ9.5eUugjqvKJs4MXIgSq5GsGuQrSPymvTacWKN08WIvKE'

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

def test_user_profile(url):
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
        'token': token0,
        'u_id': 1,
    })

    r = requests.get(url + 'user/profile?' + queryString)
    assert r.status_code == 200

    # test for a normal case
    queryString = urllib.parse.urlencode({
        'token': token1,
        'u_id': 1,
    })
    r = requests.get(url + 'user/profile?' + queryString)
    assert r.status_code == 200


def test_user_profile_setname(url):
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

    # name_first is not between 1 and 50
    r = requests.put(url + 'user/profile/setname', json={'token': token0,'name_first': 'a' * 51, 'name_last': 'a'})
    assert r.status_code == 400

    # name_last is not between 1 and 50
    r = requests.put(url + 'user/profile/setname', json={'token': token0, 'name_first': 'b', 'name_last': 'b' * 51})
    assert r.status_code == 400

    # test normal case to see the updated user details
    r = requests.put(url + 'user/profile/setname', json={'token': token3,'name_first': 'Zeyu','name_last': 'Hou'})
    assert r.status_code == 200

def test_user_profile_setemail(url):
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

    # test for invalid email addresses
    r = requests.put(url + 'user/profile/setemail', json={'token': token0,'email': '123456com'})
    assert r.status_code == 400

    # Email addressed is being used by another user
    r = requests.put(url + 'user/profile/setemail', json={'token': token0,'email': 'user1@gmail.com'})
    assert r.status_code == 400

    # test for a normal case
    r = requests.put(url + 'user/profile/setemail', json={'token': token1,'email': 'howard@gmail.com'})
    assert r.status_code == 200

def test_user_profile_sethandle(url):
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

    # handle_str must be between 3 and 20 characters
    r = requests.put(url + 'user/profile/sethandle', json={'token': token0,'handle_str': 'a'})
    assert r.status_code == 400

    # handle_str must be between 3 and 20 characters
    r = requests.put(url + 'user/profile/sethandle', json={'token': token0,'handle_str': 'a'* 21})
    assert r.status_code == 400

    # handle is already used by another user
    r = requests.put(url + 'user/profile/sethandle', json={'token': token0,'handle_str': 'hjacobs'})
    assert r.status_code == 400

    # test for a normal case 
    r = requests.put(url + 'user/profile/sethandle', json={'token': token2,'handle_str': 'whatever'})
    assert r.status_code == 200

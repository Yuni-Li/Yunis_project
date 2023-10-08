import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

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

def test_register(url):
    requests.delete(url+'clear')
    r = requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'SUPER',
        'name_last': 'USER',
    })
    assert r.status_code == 200

    # used email
    r = requests.post(url + 'auth/register', json = {
        'email': 'user0@gmail.com',
        'password': 'testtesttest',
        'name_first': 'USED',
        'name_last': 'EMAIL',
    })
    assert r.status_code == 400

    # invalid email
    r = requests.post(url + 'auth/register', json = {
        'email': 'invalid.email.com',
        'password': 'testtesttest',
        'name_first': 'INVALID',
        'name_last': 'EMAIL',
    })
    assert r.status_code == 400

    # short pw
    r = requests.post(url + 'auth/register', json = {
        'email': 'aaa@gmail.com',
        'password': '123',
        'name_first': 'INVALID',
        'name_last': 'EMAIL',
    })
    assert r.status_code == 400

    # invalid name_first
    r = requests.post(url + 'auth/register', json = {
        'email': 'aaa@gmail.com',
        'password': '111111111111',
        'name_first': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'name_last': 'EMAIL',
    })
    assert r.status_code == 400

    # invalid name_last
    r = requests.post(url + 'auth/register', json = {
        'email': 'aaa@gmail.com',
        'password': '111111111111',
        'name_first': 'AAA',
        'name_last': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    })
    assert r.status_code == 400

def test_login(url):
    requests.post(url + 'auth/register', json = {
        'email': 'user1@gmail.com',
        'password': 'fkbjvnrbvkjbdvsdvj',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
    })

    requests.post(url + 'auth/logout', json = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxfQ.ZrE0yQnKGh70FBqztJEr-2nTS_kP1BrsXH-5SMXB1Uw'})

    # invalid email
    r = requests.post(url + 'auth/login', json = {
        'email': 'user1gmail.com',
        'password': 'fkbjvnrbvkjbdvsdvj',
    })
    assert r.status_code == 400

    # Email entered does not belong to a user
    r = requests.post(url + 'auth/login', json = {
        'email': 'user2@gmail.com',
        'password': 'fkbjvnrbvkjbdvsdvj',
    })
    assert r.status_code == 400

    # incorrect pw
    r = requests.post(url + 'auth/login', json = {
        'email': 'user1@gmail.com',
        'password': 'fkbjvnrbvkjbdvsdv',
    })
    assert r.status_code == 400

    r = requests.post(url + 'auth/login', json = {
        'email': 'user1@gmail.com',
        'password': 'fkbjvnrbvkjbdvsdvj',
    })
    assert r.status_code == 200
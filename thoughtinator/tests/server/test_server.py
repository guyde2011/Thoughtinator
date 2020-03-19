from . import POST_USER, POST_SNAPSHOT
from time import sleep
from thoughtinator import server
from multiprocessing import Process

import bson
import requests


def test_upload_user(server):
    assert server.post('/user', POST_USER['in']).status_code == 200
    assert server.buffer == [POST_USER['out']]


def test_upload_snapshot(server):
    server.post('/snapshot', POST_SNAPSHOT['in'])
    sleep(0.15)
    assert server.buffer == [POST_SNAPSHOT['out']]


def test_specs():
    p = Process(target=lambda: server.run_server(host='127.0.0.1', port=3998, publish=lambda *_: 0))
    p.start()
    sleep(0.5)
    r = requests.post('http://127.0.0.1:3998/user', bson.encode(POST_USER['in']))
    assert r.status_code == 200
    p.kill()

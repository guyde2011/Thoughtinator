from thoughtinator.server import __main__ as main
import bson
from multiprocessing import Process
from time import sleep
from click import Context
import requests
from thoughtinator.utils import env


from . import *

def test_specs():
    env.os = {'SAVE_FOLDER': '/tmp/pytest/thoughtinator'}
    p = Process(target=lambda: main.command_run_server(["--host", "127.0.0.1", "--port", "3998",  "rabbitmq://127.0.0.1:1234"]))
    p.start()
    sleep(2)

    r = requests.post('http://127.0.0.1:3998/user', bson.encode(POST_USER['in']))
    assert r.status_code == 200
    p.kill()

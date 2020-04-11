from thoughtinator.server import __main__ as main
import bson
import requests
from thoughtinator.utils import env

from . import *


def test_specs(proc_runner):
    env.os = {'SAVE_FOLDER': '/tmp/pytest/thoughtinator'}

    with proc_runner(main.command_run_server, 'rabbitmq://127.0.0.1:1234', host='127.0.0.1', port='3998', delay=2):
        r = requests.post('http://127.0.0.1:3998/user', bson.encode(POST_USER['in']))
        assert r.status_code == 200

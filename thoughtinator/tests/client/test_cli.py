from . import *
import sys
import requests
from multiprocessing import Process

from thoughtinator.client import __main__ as main

def patched_post(resp):
    def patched_func(url, data):
        class PatchedResponse:
            def __init__(self):
                for key in resp:
                    setattr(self, key, resp[key])
        return PatchedResponse()
    return patched_func


def test_cli(patcher, snap_file, monkeypatch):
    buffer = patcher.patch(requests, 'post', patched_post({'status_code': 200}))
    monkeypatch.setattr(sys, 'exit', lambda *args: None)
    main.command_upload_sample(['--host', 'HOST', '--port', '3456', snap_file])
    assert buffer[0][0] == UPLOAD_USER
    assert buffer[1][0] == UPLOAD_SNAPSHOT

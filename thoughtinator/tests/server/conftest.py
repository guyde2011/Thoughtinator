import bson
import pytest

from thoughtinator.server import ServerEndpoint
from thoughtinator.utils import env


class ServerTest:
    def __init__(self):
        self.buffer = []
        self.server = ServerEndpoint(lambda *args: self.buffer.append(args))

    def post(self, url, data):
        return self.server.test_client().post(url, data=bson.encode(data))


@pytest.fixture
def server():
    env.os = {'SAVE_FOLDER': '/tmp/pytest/thoughtinator'}
    return ServerTest()

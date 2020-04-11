import requests
import bson

from thoughtinator.utils import logger
from thoughtinator.client.reader import drivers


def upload_sample(path: str,
                  host: str,
                  port: int = 8000,
                  file_format: str = 'protobuf'):
    """Uploads a sample file with to a remote host
    :type path: str
    :param path: the path to the sample file

    :type host: str
    :param host: the host of the upload server

    :type port: int
    :param port: the port of the upload server

    :type file_format: str
    :param file_format: the format of the sample file
    """
    file_reader = drivers[file_format](path)
    posted_user = False
    for snap in file_reader.read():
        if not posted_user:
            _post_user(file_reader.user, host, port)
            posted_user = True
        _post_snapshot(snap, file_reader.user, host, port)


def _post_user(user: dict, host: str, port: int):
    resp = requests.post(f'http://{host}:{port}/user',
                         bson.encode(user))
    if resp.status_code == 200:
        return
    logger.error(f'Failed to send user to server \n\t> {resp.status_code}')


def _post_snapshot(snap: dict, user: dict, host: str, port: int):
    snap['user_id'] = user['user_id']
    resp = requests.post(f'http://{host}:{port}/snapshot',
                         bson.encode(snap))
    if resp.status_code == 200:
        return
    logger.error(f'Failed to send snapshot to server \n\t> {resp.status_code}')

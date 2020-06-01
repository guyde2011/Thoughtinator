import requests

from . import TEMP_FILE, UPLOAD_SNAPSHOT, UPLOAD_USER

from thoughtinator.client import upload_sample


def patched_post(resp):
    def patched_func(url, data):
        class PatchedResponse:
            def __init__(self):
                for key in resp:
                    setattr(self, key, resp[key])
        return PatchedResponse()
    return patched_func


def test_upload(patcher, snap_file):
    buffer = patcher.patch(requests, 'post', patched_post({'status_code': 200}))
    upload_sample(path=snap_file, host='HOST', port=3456, file_format='protobuf')
    assert buffer[0][0] == UPLOAD_USER
    assert buffer[1][0] == UPLOAD_SNAPSHOT


import gzip

from . import TEMP_FILE, RAW_SNAPSHOTS, RAW_USER, USER, SNAPSHOT

import struct

from google.protobuf.json_format import MessageToDict

def test_protobuf_load():
    from thoughtinator.client.reader import drivers
    assert 'protobuf' in drivers


def test_protobuf_read(snap_file):
    from thoughtinator.client.reader import drivers
    protobuf = drivers['protobuf']
    pb = protobuf(snap_file)
    snap = next(pb.read())
    user = pb.user
    user['gender'] = user['gender'] if 'gender' in user else 0
    assert user == USER
    assert snap == SNAPSHOT

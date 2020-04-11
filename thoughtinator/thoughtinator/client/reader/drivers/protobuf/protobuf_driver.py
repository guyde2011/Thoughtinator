import gzip
import struct

from google.protobuf.json_format import MessageToDict

from .thoughtinator_pb2 import Snapshot, User

from thoughtinator.client.reader import ReaderDriver


class ProtobufDriver(ReaderDriver):
    def __init__(self, path: str):
        self._path = path
        self._user = User()  # type: ignore

    @property
    def user(self):
        ret = MessageToDict(self._user, preserving_proto_field_name=True,
                            including_default_value_fields=True)
        ret['user_id'] = int(ret['user_id'])
        ret['gender'] = {'MALE': 0, 'FEMALE': 1, 'OTHER': 2}[ret['gender']]
        return ret

    def read(self):
        with gzip.open(self._path) as f:
            size, = struct.unpack('I', f.read(4))
            self._user.ParseFromString(f.read(size))
            while True:
                try:
                    size, = struct.unpack('I', f.read(4))
                    total_read = 0
                    reads = []
                    snap = Snapshot()
                    while total_read < size:
                        reads.append(f.read(size - total_read))
                        total_read += len(reads[-1])
                    snap.ParseFromString(b''.join(reads), )
                except struct.error:
                    return
                ret = MessageToDict(snap, preserving_proto_field_name=True,
                                    including_default_value_fields=True)
                ret['color_image']['data'] = snap.color_image.data
                yield ret

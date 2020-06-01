import gzip
import pytest

import struct
from . import TEMP_FILE, RAW_SNAPSHOTS, RAW_USER, USER, SNAPSHOT

@pytest.fixture
def snap_file(tmp_path):
    path = tmp_path / 'sample.gz'
    with gzip.open(str(path), 'w') as f:
        f.write(struct.pack('I', len(RAW_USER)))
        f.write(RAW_USER)
        f.write(struct.pack('I', len(RAW_SNAPSHOTS)))
        f.write(RAW_SNAPSHOTS)
    return str(path)
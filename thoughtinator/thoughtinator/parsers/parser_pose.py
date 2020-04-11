import bson

from . import parser


@parser.of('pose')
def parse_pose(data: str) -> str:
    j_data = bson.decode(data)
    return bson.encode({
        'data': j_data['pose'],
        'datetime': j_data['datetime'],
        'snap_id': j_data['snap_id'],
        'user_id': j_data['user_id'],
    })

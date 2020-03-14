import bson

from . import parser


@parser.of('feelings')
def parse_feelings(data: str) -> str:
    j_data = bson.decode(data)
    return bson.encode({
        'data': j_data['feelings'],
        'datetime': j_data['datetime'],
        'snap_id': j_data['snap_id'],
        'user_id': j_data['user_id'],
    })

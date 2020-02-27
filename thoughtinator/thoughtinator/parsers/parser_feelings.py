import json

from . import parser


@parser.of('feelings')
def parse_feelings(data: str) -> str:
    j_data = json.loads(data)
    return json.dumps({
        'data': j_data['feelings'],
        'datetime': j_data['datetime'],
        'user_id': j_data['user_id'],
    })

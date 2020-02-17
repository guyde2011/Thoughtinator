import json

from thoughtinator.parsers import parser

@parser.of('pose')
def parse_pose(data: str) -> str:
    """ Description
    :type data: str
    :param data: 

    :rtype: str
    """ 
    j_data = json.loads(data)
    
    return json.dumps({
        'data': j_data['pose'],
        'datetime': j_data['datetime'],
        'user_id': j_data['user_id'],
    })
    
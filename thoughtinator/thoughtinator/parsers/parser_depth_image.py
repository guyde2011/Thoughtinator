import json
import numpy
import matplotlib.pyplot as pyplot

from pathlib import Path
from typing import cast

from thoughtinator.utils import env
from parsers import parser

DEFAULT_FOLDER = '{}/parsed'.format(env.os['SAVE_FOLDER'] or '/thoughtbase')

@parser.of('depth_image')
def parse_depth_image(data: str, folder: str = DEFAULT_FOLDER) -> str:
    j_data = json.loads(data)
    path = Path(folder)
    img_path = \
        path / str(j_data['user_id']) / j_data['datetime']

    _save_image(cast(dict, j_data['depth_image']), img_path)

    return json.dumps({
        'data': {'path': str(path) / 'depth_image.jpg'},
        'datetime': j_data['datetime'],
        'user_id': j_data['user_id'],
    })
    
def _save_image(data: dict, path: Path):
    if not path.exists():
        path.mkdir(parents=True)

    f_data = np.load(data['path'])
    img = f_data.reshape(f_data['width'], f_data['height'])
    pyplot.imshow(img)
    pyplot.savefig(path / 'depth_image.jpg')

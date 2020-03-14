import bson

from pathlib import Path
from PIL import Image
from typing import cast

from thoughtinator.utils import env
from . import parser

DEFAULT_FOLDER = '{}/parsed'.format(env.os['SAVE_FOLDER'] or '/thoughtbase')


@parser.of('color_image')
def parse_color_image(data: str, folder: str = DEFAULT_FOLDER) -> str:
    j_data = bson.decode(data)
    path = Path(folder)
    img_path = \
        path / str(j_data['user_id']) / j_data['datetime']

    _save_image(cast(dict, j_data['color_image']), img_path)

    return bson.encode({
        'data': {'path': str(img_path / 'color_image.jpg')},
        'datetime': j_data['datetime'],
        'snap_id': j_data['snap_id'],
        'user_id': j_data['user_id'],
    })


def _save_image(data: dict, path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    with open(data['path'], 'rb') as img_file:
        f_data = img_file.read()

    img = Image.frombytes('RGB',
                          (data['width'], data['height']),
                          f_data)
    img.save(path / 'color_image.jpg')

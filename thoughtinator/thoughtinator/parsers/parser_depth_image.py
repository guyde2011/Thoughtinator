import bson
import numpy
import matplotlib.pyplot as pyplot

from pathlib import Path
from typing import cast

from thoughtinator.utils import env
from . import parser

DEFAULT_FOLDER = '{}/parsed'.format(env.os['SAVE_FOLDER'] or '/thoughtbase')


@parser.of('depth_image')
def parse_depth_image(data: str, folder: str = DEFAULT_FOLDER) -> str:
    j_data = bson.decode(data)
    path = Path(folder)
    img_path = \
        path / str(j_data['user_id']) / j_data['datetime']

    _save_image(cast(dict, j_data['depth_image']), img_path)

    return bson.encode({
        'data': {'path': str(img_path / 'depth_image.jpg')},
        'datetime': j_data['datetime'],
        'snap_id': j_data['snap_id'],
        'user_id': j_data['user_id'],
    })


def _save_image(data: dict, path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    f_data = numpy.load(data['path'])
    img = f_data.reshape((data['height'], data['width']))
    pyplot.imshow(img)
    pyplot.savefig(path / 'depth_image.jpg')

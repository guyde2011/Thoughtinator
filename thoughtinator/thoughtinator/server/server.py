import flask


from furl import furl
from pathlib import Path
from typing import Optional
from json import dumps as json_dumps

from thoughtinator import mqueue
from thoughtinator.utils import logger, env


class ServerEndpoint:
    def __init__(self,
                 host: str,
                 port: int,
                 mqueue_url: str,
                 *,
                 path: Optional[Path] = None):
        self.mqueue_url = furl(mqueue_url)
        self.app = flask.Flask('thoughtinator3000')
        self.host = host
        self.port = port
        self.app.route('/snapshot', methods=['POST'])(self._load_snapshot)
        self.path: Path = path or Path(env.os['SAVE_FOLDER'])

    def _load_snapshot(self):
        try:
            json: dict = flask.request.get_json()
        except BaseException as e:
            logger.warning(f'Malformed json from user\n\t  > {e}')
            return {'success': False, 'error': 'Malformed JSON'}, 400
        try:
            path = self.path / str(json['user']['user_id']) / json['datetime']
            self._save_snapshot(json, path=path)
            json['color_image'].pop('data')
            json['depth_image'].pop('data')
            json['color_image']['path'] = str(path / 'color_image.jpg')
            json['depth_image']['path'] = str(path / 'depth_image.jpg')
        except BaseException as e:
            logger.warning(f'Invalid json from user\n\t  > {e}')
            return {'error': 'Invalid JSON'}, 418
        self._publish_snapshot(json_dumps(json), json_dumps(json['user']))
        return {}, 200

    def run(self):
        self.app.run(self.host, self.port)

    def _save_snapshot(self, json: dict, *, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        (path / 'color_image.jpg').write_bytes(
            json['color_image']['data'].encode('latin1'))
        (path / 'depth_image.jpg').write_bytes(
            json['depth_image']['data'].encode('latin1'))

    def _publish_snapshot(self, data: str, user: str):
        host = self.mqueue_url.host
        port = self.mqueue_url.port
        scheme = self.mqueue_url.scheme
        driver = mqueue[scheme](host, port)
        driver.publish_work(user, route='data', exchange='thoughtinator.user')
        driver.publish_data(data, exchange='thoughtinator.work')

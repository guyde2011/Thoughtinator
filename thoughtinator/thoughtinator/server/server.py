import flask
import bson

from pathlib import Path
from typing import Optional, Callable
from threading import Thread, Lock
import numpy as np

from thoughtinator.utils import logger, env, FlaskEndpoint


class ServerEndpoint(FlaskEndpoint):
    def __init__(self,
                 publish: Callable,
                 *,
                 path: Optional[Path] = None):
        super().__init__('thoughtinator/server')
        self.publish = publish
        self.path: Path = path or Path(env.os['SAVE_FOLDER'])
        self._snap_id: int = 0
        self._lock: Lock = Lock()
        self.driver = publish

    def snap_id(self):
        with self._lock:
            ret = self._snap_id
            self._snap_id += 1
        return ret

    @route('/snapshot', methods=['POST'])
    def load_snapshot(self):
        try:
            json: dict = bson.decode(flask.request.get_data())
        except BaseException as e:
            logger.warning(f'Malformed json from user\n\t  > {e}')
            return {'error': 'Malformed JSON'}, 400

        snap_id = self.snap_id()
        json['snap_id'] = snap_id
        Thread(target=lambda: self._handle_snapshot(json)).start()
        return {'id': snap_id}, 200

    def _handle_snapshot(self, json: dict):
        path = self.path / str(json['user_id']) / str(json['datetime'])
        self._save_snapshot(json, path=path)
        json['color_image'].pop('data')
        json['depth_image'].pop('data')
        json['color_image']['path'] = str(path / 'color_image.raw')
        json['depth_image']['path'] = str(path / 'depth_image.npy')
        self._publish_snapshot(bson.encode(json))

    @route('/user', methods=['POST'])
    def load_user(self):
        try:
            json: dict = bson.decode(flask.request.get_data())
        except BaseException as e:
            logger.warning(f'Malformed json from user\n\t  > {e}')
            return {'error': 'Malformed JSON'}, 400
        Thread(target=lambda: self._publish_user(bson.encode(json))).start()
        return '', 200

    def _save_snapshot(self, json: dict, *, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        (path / 'color_image.raw').write_bytes(
            json['color_image']['data'])

        np.save(str(path / 'depth_image.npy'),
                np.array(json['depth_image']['data']))

    def _publish_snapshot(self, snap: str):
        self.driver(snap, 'thoughtinator.raw')

    def _publish_user(self, user: str):
        self.driver(user, 'thoughtinator.out', 'user')

from typing import List, Optional
from pymongo import MongoClient

from thoughtinator.database import DatabaseDriver, User, Snapshot


class MongoDriver(DatabaseDriver):

    def __init__(self, url: str):
        self.client = MongoClient(url)['thoughtinator']

        self.savers = {
            'pose':
                lambda snap: self._update_snapshot(snap, 'pose'),
            'color_image':
                lambda snap: self._update_snapshot(snap, 'color_image'),
            'depth_image':
                lambda snap: self._update_snapshot(snap, 'depth_image'),
            'feelings':
                self._update_feelings,
            'user':
                lambda user: self.put_user(user)
        }

    def _update_snapshot(self, snap, field):
        self.client.snapshots.update_one(
            {'snap_id': snap['snap_id']},
            {'$set': {field: snap['data'],
                      'snap_id': snap['snap_id'],
                      'datetime': snap['datetime'],
                      'user_id': snap['user_id']}},
            upsert=True)

    def _update_feelings(self, snap):
        feelings = {feel: 0.0 for feel in
                    ['thirst', 'exhaustion', 'hunger', 'happiness']}
        feelings.update(snap['data'])
        self.client.snapshots.update_one(
            {'snap_id': snap['snap_id']},
            {'$set': {'feelings': feelings,
                      'snap_id': snap['snap_id'],
                      'datetime': snap['datetime'],
                      'user_id': snap['user_id']}},
            upsert=True)

    def fetch_users(self) -> List[User]:
        return list(self.client.user_list.find({}, {'_id': 0}))
        # type: ignore

    def fetch_user(self, user_id: int) -> Optional[User]:
        org = {'gender': 0}
        dct = self.client.user_list.find_one({'user_id': user_id}, {'_id': 0})
        dct.update(org)
        return dct
        # type: ignore

    def fetch_snapshots(self, user_id: int) -> Optional[List[Snapshot]]:
        ret = self.client.snapshots.find({'user_id': user_id}, {'_id': 0})
        if ret is None:
            return None
        return list(ret)
        # type: ignore

    def fetch_snapshot(self, snap_id: int) -> Optional[Snapshot]:
        return self.client.snapshots.find_one({'snap_id': snap_id}, {'_id': 0})
        # type: ignore

    def put_user(self, user: User):
        self.client['user_list'].update_one({'user_id': user['user_id']},
                                            {'$set': user},
                                            upsert=True)

    def put_snapshot(self, snapshot: Snapshot):
        self.client.snapshots.update_one({'snap_id': snapshot},
                                         {'$set': snapshot},
                                         upsert=True)

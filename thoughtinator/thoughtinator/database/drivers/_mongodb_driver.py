from typing import List, Optional
from pymongo import MongoClient

from ..database import DatabaseDriver, User, Snapshot


class MongoDriver(DatabaseDriver):

    def __init__(self, url: str):
        self.client = MongoClient(url)

    def fetch_users(self) -> List[User]:
        return list(self.client.user_list.find())
        # type: ignore

    def fetch_user(self, user_id: int) -> Optional[User]:
        return self.client.user_list.find_one({'user_id': user_id})
        # type: ignore

    def fetch_snapshots(self, user_id: int) -> Optional[List[Snapshot]]:
        return self.client.snapshots.find({'user_id': user_id})
        # type: ignore

    def fetch_snapshot(self, snap_id: int) -> Optional[Snapshot]:
        return self.client.snapshots.find_one({'snap_id': snap_id})
        # type: ignore

    def put_user(self, user: User):
        self.client.user_list.insert_one(user)

    def put_snapshot(self, snapshot: Snapshot):
        self.client.snapshots.insert_one(snapshot)

import flask

from flask_cors import CORS
from furl import furl
from typing import List

from thoughtinator.utils import FlaskEndpoint
import thoughtinator.database.drivers as db_drivers
from thoughtinator.database import Database


class API(FlaskEndpoint):

    def __init__(self, db_url: str, *, fields: List[str] = []):
        super().__init__('thoughtinator3000/api')
        self.database = Database(db_drivers[furl(db_url).scheme](db_url))
        self._fields = [f.replace('-', '_') for f in fields]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        CORS(self.app)

    @route('/users')
    def fetch_users(self):
        users = list(self.database.users)
        formatted_users = [
            {key: user[key] for key in ['user_id', 'username']}
            for user in users]
        return flask.jsonify(formatted_users), 200

    @route('/users/<int:user_id>')
    def fetch_user(self, user_id: int):
        user = self.database.users[user_id]
        if user:
            return user, 200
        return '', 404

    @route('/users/<int:user_id>/snapshots')
    def fetch_snapshots(self, user_id: int):
        snapshots = self.database.snapshots[self.database.users[user_id]]
        if snapshots:
            snapshots = [
                {key: snap[key] for key in ['snap_id', 'datetime']}
                for snap in snapshots]
            return flask.jsonify(snapshots), 200
        return '', 404

    @route('/users/<int:user_id>/snapshots/<int:snap_id>')
    def fetch_snapshot(self, user_id: int, snap_id: int):
        snapshot = self.database.snapshots[snap_id]
        if snapshot and snapshot['user_id'] == user_id:
            fields = filter(lambda key: key in self._fields, snapshot.keys())
            fields = list(fields)  # type: ignore
            snapshot['fields'] = list(fields)
            return {key: snapshot[key] for key in snapshot
                    if key not in fields}, 200

        return '', 404

    @route('/users/<int:user_id>/snapshots/<int:snap_id>/<field>')
    def fetch_field(self, user_id: int, snap_id: int, field: str):
        field = field.replace('-', '_')
        snapshot = self.database.snapshots[snap_id]
        if snapshot \
           and snapshot['user_id'] == user_id \
           and field in snapshot \
           and field in self._fields:
            return snapshot[field], 200
        return '', 404

    @route('/users/<int:user_id>/snapshots/<int:snap_id>/<field>/data')
    def fetch_data(self, user_id: int, snap_id: int, field: str):
        field = field.replace('-', '_')
        snapshot = self.database.snapshots[snap_id]
        if snapshot \
           and snapshot['user_id'] == user_id \
           and field in snapshot \
           and field in self._fields \
           and 'path' in snapshot[field]:
            return flask.send_file(snapshot[field]['path'])
        return '', 404

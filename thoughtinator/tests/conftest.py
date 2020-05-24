import pytest
import sys
import time

from typing import List, Optional
from pymongo import MongoClient

from thoughtinator.database import DatabaseDriver, User, Snapshot, Database
from thoughtinator.api import APIEndpoint

from multiprocessing import Process


class MockDBDriver(DatabaseDriver):
    def __init__(self):
        self.users, self.snapshots = {}, {}

    def fetch_users(self) -> List[User]:
        return list(self.users.values())

    def fetch_user(self, user_id: int) -> Optional[User]:
        return self.users[user_id] if user_id in self.users else None

    def fetch_snapshots(self, user_id: int) -> Optional[List[Snapshot]]:
        lst = \
            filter(lambda s: s['user_id'] == user_id, self.snapshots.values())
        return list(lst)

    def fetch_snapshot(self, snap_id: int) -> Optional[Snapshot]:
        return self.snapshots[snap_id] if snap_id in self.snapshots else None

    def put_snapshot(self, snapshot: Snapshot):
        self.snapshots[snapshot['snap_id']] = snapshot


    def put_user(self, user: User):
        self.users[user['user_id']] = user


@pytest.fixture
def cli_runner(monkeypatch):
    def run_cli(cmd, *args, **kwargs):
        total = []
        for k, v in kwargs.items():
            total += [f'--{k}', v]
        total += args
        monkeypatch.setattr(sys, 'exit', lambda *args, **kwargs: None)
        return cmd(total)
    return run_cli


class ProcCM:
    def __init__(self, proc, delay):
        self.proc = proc
        self.delay = delay

    def __enter__(self):
        self.proc.start()
        if self.delay:
            time.sleep(self.delay)
        return self

    def __exit__(self, cls, exception, tb):
        self.proc.kill()


@pytest.fixture
def proc_runner(monkeypatch):
    def run_cli(cmd, *args, delay=None, **kwargs):
        total = []
        for k, v in kwargs.items():
            total += [f'--{k}', v]
        total += args

        def run():
            monkeypatch.setattr(sys, 'exit', lambda *args, **kwargs: None)
            cmd(total)
        return ProcCM(Process(target=run), delay)     

    return run_cli


@pytest.fixture
def db_driver():
    import thoughtinator.database.drivers as drivers
    driver = MockDBDriver()
    drivers._comps['mock'] = lambda *args: driver
    return driver


@pytest.fixture
def api_requests(db_driver):
    api = APIEndpoint('mock://127.0.0.1:1245',
              fields=['pose', 'feelings', 'color_image', 'depth_image'])
    api.database = Database(db_driver)
    return api.test_client(), db_driver


class Patcher:

    def __init__(self, mp):
        self.mp = mp

    def patch(self, obj, member, func=lambda *a, **kw: None):
        buffer = []
        self.mp.setattr(obj, member, patched(buffer, func))
        return buffer

@pytest.fixture
def patcher(monkeypatch):
    return Patcher(monkeypatch)


def patched(buffer, func):
    def wrapped_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        buffer.append((args, kwargs, ret))
        return ret
    return wrapped_func

import json

from . import *
import requests


def test_get_users(api_requests):
    api, db = api_requests
    db.put_user(USER)
    assert api.get('/users').json == [{'user_id': USER['user_id'], 'username': USER['username']}]


def test_get_user(api_requests):
    api, db = api_requests
    db.put_user(USER)
    assert api.get('/users/1').json == USER


def test_get_snapshots(api_requests):
    api, db = api_requests
    db.put_user(USER)
    db.put_snapshot(SNAPSHOT)
    assert api.get('/users/1/snapshots').json == [{'snap_id': SNAPSHOT['snap_id'], 'datetime': SNAPSHOT['datetime']}]


def test_get_snapshot(api_requests):
    api, db = api_requests
    db.put_user(USER)
    db.put_snapshot(SNAPSHOT)
    assert api.get('/users/1/snapshots/2').json == {'user_id': SNAPSHOT['user_id'], 'snap_id': SNAPSHOT['snap_id'], 'datetime': SNAPSHOT['datetime'], 'fields': ['feelings', 'pose', 'color_image', 'depth_image']}


def test_get_simple_field(api_requests):
    api, db = api_requests
    db.put_user(USER)
    db.put_snapshot(SNAPSHOT)
    assert api.get('/users/1/snapshots/2/pose').json == POSE


def test_get_data_field(api_requests):
    api, db = api_requests
    db.put_user(USER)
    db.put_snapshot(SNAPSHOT)
    assert api.get('/users/1/snapshots/2/color_image').json == COLOR_IMAGE


def test_cli(db_driver, proc_runner):
    from thoughtinator.api import __main__ as main
    db_driver.put_user(USER)
    with proc_runner(main.command_run_server, delay=0.75, host='127.0.0.1', port='1144', database='mock://127.0.0.1:1234'):
        assert requests.get('http://127.0.0.1:1144/users').json() == [{'user_id': USER['user_id'], 'username': USER['username']}]

import click
import sys
import requests
import urllib


from furl import furl

@click.group()
def cli():
    pass


@cli.command('get-user')        
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
def command_get_user(host, port, user_id):
    print(requests.get(f'http://{host}:{port}/users/{user_id}').json())


@cli.command('get-users')        
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
def command_get_users(host, port):
    print(requests.get(f'http://{host}:{port}/users').json())


@cli.command('get-snapshots')        
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
def command_get_snapshots(host, port, user_id):
    print(requests.get(f'http://{host}:{port}'
                       f'/users/{user_id}/snapshots').json())


@cli.command('get-snapshot')        
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
@click.argument('snap_id', type=int)
def command_get_snapshot(host, port, user_id, snap_id):
    print(requests.get(f'http://{host}:{port}'
                       f'/users/{user_id}/snapshots/{snap_id}').json())


@cli.command('get-result')        
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.option('-s', '--save', default='', type=str)
@click.argument('user_id', type=int)
@click.argument('snap_id', type=int)
@click.argument('result', type=str)
def command_get_result(host, port, save, user_id, snap_id, result):
    resp = requests.get(f'http://{host}:{port}'
                        f'/users/{user_id}/snapshots/{snap_id}').json()
    print(resp)
    if save:
        path = resp['path']
        url = furl()
        url.set(scheme='http', host=host, port=port, path=path)
        urllib.request.urlretrieve(url.url, save)


if __name__ == '__main__':
    sys.exit(cli())

import click
import sys

from . import APIEndpoint


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h', required=True, type=str)
@click.option('--port', '-p', required=True, type=int)
@click.option('--database', '-d', required=True, type=str)
def command_run_server(host: str, port: int, database: str):
    api = APIEndpoint(database, fields=['pose',
                                        'color-image',
                                        'depth-image',
                                        'feelings'])
    api.run(host, port)


if __name__ == '__main__':
    sys.exit(cli())

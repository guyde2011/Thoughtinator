import click
import sys

from . import ServerEndpoint


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h', required=True, type=str)
@click.option('--port', '-p', required=True, type=int)
@click.argument('mqueue_url', type=str)
def command_run_server(host, port, mqueue_url):
    endpoint = ServerEndpoint(mqueue_url)
    endpoint.run(host, port)


if __name__ == '__main__':
    sys.exit(cli())

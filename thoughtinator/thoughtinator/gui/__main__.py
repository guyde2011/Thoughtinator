from . import run_server

import click
import sys


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h', required=True, type=str)
@click.option('--port', '-p', required=True, type=int)
@click.option('--api-host', '-H', required=True, type=str)
@click.option('--api-port', '-P', required=True, type=int)
def command_run_server(host, port, api_host, api_port):
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    sys.exit(cli())

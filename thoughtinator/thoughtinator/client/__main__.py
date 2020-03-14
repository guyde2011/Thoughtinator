import click
import sys

from . import upload_sample


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', required=True, type=str)
@click.option('-p', '--port', required=True, type=int)
@click.argument('path', type=str)
def command_upload_sample(host, port, path):
    upload_sample(path=path, host=host, port=port)


if __name__ == '__main__':
    sys.exit(cli())

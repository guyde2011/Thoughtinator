import click
import furl
import sys

from pathlib import Path

from thoughtinator.utils import logger, env
from . import parser
error = logger.error(forbid=['hide-click-errors'])

@click.group()
def cli():
    pass

schemes = {}

@cli.command('run-parser')
@click.argument('field')
@click.argument('url')
def run_parser(field, url):
    scheme = furl.furl(url).scheme
    if scheme not in schemes:
        error(f'Scheme `{scheme}` not supported', func=click.echo)
        return
    schemes[scheme](field)


@cli.command('parse')
@click.argument('field')
@click.argument('file_name')
def cli_command_parse(field, file_name):
    if not Path(file_name).exists():
        error(f'File `{file_name}` does not exist', func=click.echo)
        return

    if field not in parser.parsers:
        error(f'Parser `{field}` does not exist', func=click.echo)
        return

    with open(file_name, 'r') as f:
        data = f.read()

    parser.parsers[field](data)

if __name__ == '__main__':
    sys.exit(cli())
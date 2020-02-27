import click
import sys

from pathlib import Path
from furl import furl

from thoughtinator.utils import logger, env, ansi
import thoughtinator.mqueue as mqueue
from . import parser


@click.group()
def cli():
    pass


@cli.command('run-parser')
@click.argument('field')
@click.argument('url')
def command_run_parser(field, url):
    scheme = furl(url).scheme
    if scheme not in mqueue:
        logger.error(f'Scheme {ansi.bold(scheme)} not supported')
        return
    env.props['mqueue_url'] = url
    mqueue[scheme].publish


@cli.command('parse')
@click.argument('field')
@click.argument('filename')
def command_parse(field, filename):
    if not Path(filename).exists():
        logger.error(f'File {ansi.bold(filename)} does not exist')
        return

    if field not in parser:
        logger.error(f'Parser {ansi.bold(field)} does not exist')
        return

    with open(filename, 'r') as f:
        data = f.read()

    print(parser[field](data))


if __name__ == '__main__':
    sys.exit(cli())

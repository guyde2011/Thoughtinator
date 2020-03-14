import click
import sys

from pathlib import Path
from furl import furl

from thoughtinator.utils import logger, ansi
import thoughtinator.mqueue.drivers as drivers
from . import parser


@click.group()
def cli():
    pass


@cli.command('run-parser')
@click.argument('field', type=str)
@click.argument('url', type=str)
def command_run_parser(field, url):
    f_url = furl(url)
    scheme = f_url.scheme
    if scheme not in drivers:
        logger.error(f'Scheme {ansi.bold(scheme)} not supported')
        return

    driver = drivers[scheme](f_url.host, f_url.port)

    def handler(route, data):
        driver.publish_data(parser[field](data), 'thoughtinator.out', field)

    driver.consume_work(handler, 'thoughtinator.raw', field)


@cli.command('parse')
@click.argument('field', type=str)
@click.argument('filename', type=str)
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

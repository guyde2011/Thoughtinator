import click
import sys

from . import ServerEndpoint
from thoughtinator.utils import logger, ansi
from thoughtinator.mqueue import drivers
from furl import furl


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('--host', '-h', required=True, type=str)
@click.option('--port', '-p', required=True, type=int)
@click.argument('mqueue_url', type=str)
def command_run_server(host, port, mqueue_url):
    url = furl(mqueue_url)
    if url.scheme not in drivers:
        logger.error(f'Scheme {ansi.bold(url.scheme)} is invalid')
    driver = drivers[url.scheme](url.host, url.port)

    def make_publish(*args):
        if len(args) < 3:
            return driver.publish_work(*args)
        return driver.publish_data(*args)
    endpoint = ServerEndpoint(make_publish)
    endpoint.run(host, port)


if __name__ == '__main__':
    sys.exit(cli())

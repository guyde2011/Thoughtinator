import click

from furl import furl

from . import Saver

import thoughtinator.mqueue.drivers as drivers


@click.group()
def cli():
    pass


@cli.command('run-saver')
@click.argument('database', type=str)
@click.argument('message_queue', type=str)
def command_run_saver(database, message_queue):
    saver = Saver(database)
    mq_url = furl(message_queue)
    driver = drivers[mq_url.scheme](mq_url.host, mq_url.port)
    driver.consume_data(saver.save,
                        'thoughtinator.out',
                        ['user',
                         'pose',
                         'color_image',
                         'depth_image',
                         'feelings'],
                        )


if __name__ == '__main__':
    cli()

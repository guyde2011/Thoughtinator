import bson

from furl import furl

from thoughtinator.database import Database, drivers
from thoughtinator.utils import logger, ansi


class Saver:
    def __init__(self, url: str):
        self.url = furl(url)
        self.db = Database(drivers[self.url.scheme](url))

    def save(self, saver: str, data: str):
        logger.info(f'Running saver {ansi.bold(saver)}')
        self.db.savers[saver](bson.decode(data))

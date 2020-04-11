import bson

from furl import furl

from thoughtinator.database import Database, drivers
from thoughtinator.utils import logger, ansi


class Saver:
    def __init__(self, url: str):
        """ Creates a new saver wrapper
        :type url: str
        :param url: the url of the database
        """
        self.url = furl(url)
        self.db = Database(drivers[self.url.scheme](url))

    def save(self, saver: str, data: bytes):
        """ Saves a given data for a given topic in the database
        :type saver: str
        :param saver: the saver to use

        :type data: bytes
        :param data: the data to save
        """
        logger.info(f'Running saver {ansi.bold(saver)}')
        self.db.savers[saver](bson.decode(data))

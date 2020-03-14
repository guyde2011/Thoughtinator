from thoughtinator.utils import logger
from thoughtinator.utils import ModuleLoader


if __name__ == 'thoughtinator.mqueue.drivers':
    mqueue = ModuleLoader()
    logger.info('Loading message queue drivers')
    mqueue.load_modules('thoughtinator.mqueue.drivers')
    mqueue.bind(__name__)

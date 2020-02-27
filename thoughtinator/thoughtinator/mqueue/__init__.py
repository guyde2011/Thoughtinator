from thoughtinator.utils import env
from thoughtinator.utils import ModuleLoader


if __name__ == 'thoughtinator.mqueue':
    mqueue = ModuleLoader()
    mqueue.load_modules(env.root / 'thoughtinator' / 'mqueue')
    mqueue.bind(__name__)

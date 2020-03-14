from thoughtinator.utils import ModuleLoader


if __name__ == 'thoughtinator.database.drivers':
    drivers = ModuleLoader()
    drivers.load_modules('thoughtinator.database.drivers')
    drivers.bind(__name__)

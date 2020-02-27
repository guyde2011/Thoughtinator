from thoughtinator.utils import ModuleLoader, env


if __name__ == 'thoughtinator.database.drivers':
    drivers = ModuleLoader()
    drivers.load_modules(env.root / 'thoughtinator' / 'database' / 'drivers')
    drivers.bind(__name__)

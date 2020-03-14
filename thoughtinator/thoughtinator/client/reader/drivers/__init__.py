from thoughtinator.utils import ModuleLoader


if __name__ == 'thoughtinator.client.reader.drivers':
    reader = ModuleLoader()
    reader.load_modules('thoughtinator.client.reader.drivers')
    reader.bind(__name__)

import flask
import time

from pathlib import Path
from thoughtinator.utils import FlaskEndpoint


class GUI(FlaskEndpoint):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.folder = Path(__file__).parent / 'react/thoughtinator-gui/build'
        super().__init__('thoughtinator-gui',
                         template_folder=str(self.folder),
                         static_folder=str(self.folder / 'static')
                         )

    @route('/')
    def serve_main(self):
        return flask.render_template('index.html',
                                     api_host=self.host,
                                     api_port=self.port)

    @route('/<path:file>')
    def serve_file(self, file):
        path = self.folder / file
        if path.exists():
            return flask.send_file(path)
        return '', 404

import flask
import time

from pathlib import Path
from thoughtinator.utils import FlaskEndpoint


class GUI(FlaskEndpoint):

    def __init__(self):
        folder = Path(__file__).parent / 'react/thoughtinator-gui/build'
        super().__init__('thoughtinator-gui',
                         template_folder=str(folder),
                         static_folder=str(folder / 'static')
                         )

    @route('/time')
    def get_current_time(self):
        return flask.render_template('index.html')

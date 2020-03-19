from . import *


def test_parsers_load():
    from thoughtinator.parsers import parser
    assert all([f in parser for f in PARSER_FIELDS])

def test_color_image():
    from thoughtinator.parsers import parser
    parser['color_image']
    
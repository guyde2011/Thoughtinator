from . import *
import bson


def test_parsers_load():
    from thoughtinator.parsers import parser
    assert all([f in parser for f in PARSER_FIELDS])


def test_color_image():
    from thoughtinator.parsers import parser
    parser['color_image']


def test_cli(cli_runner, tmp_path, capsys):
    from thoughtinator.parsers import __main__ as main
    path = tmp_path / 'tmp_file'
    path.write_bytes(bson.encode(SNAPSHOT))
    cli_runner(main.command_parse, 'feelings', str(path))
    assert capsys.readouterr().out == str(RAW_SNAPSHOT) + '\n'

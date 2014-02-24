import argparse

from database import Db, Show




parser = argparse.ArgumentParser(description='ShowPy manages your shows.', prog='ShowPy')
# set metavar to avoid {commands} printing
commands = parser.add_subparsers(title='Commands', metavar='')
commands.add_parser('help', help='Show help for command.')


def add_show(args):
    Show.save_multiple(Show(title=title) for title in args.title)

add_parser = commands.add_parser('add', help='Add show to collection.')
add_parser.add_argument('title', nargs='+')
add_parser.set_defaults(func=add_show)


def list_shows(args):
    print Show.all()

add_parser = commands.add_parser('list', help='List all shows in collection.')
add_parser.set_defaults(func=list_shows)


db = Db.instance()
args = parser.parse_args()
args.func(args)

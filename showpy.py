import argparse

from database import Show


parser = argparse.ArgumentParser(description='ShowPy manages your shows.', prog='ShowPy')
# set metavar to avoid {commands} printing
commands = parser.add_subparsers(title='Commands', metavar='')
commands.add_parser('help', help='Show help for command.')


class _Command(type):
    def __new__(meta, name, bases, dct):
        print '-----------------------------------'
        print "Allocating memory for class", name
        print meta
        print bases
        print dct
        return super(_Command, meta).__new__(meta, name, bases, dct)
    def __init__(cls, name, bases, dct):
        print '-----------------------------------'
        print "Initializing class", name
        print cls
        print bases
        print dct
        super(_Command, cls).__init__(name, bases, dct)

class Command(_Command('CommandMeta', (object,), {})):
    def run(self):
        print 'hmm'

def add_show(args):
    Show.save_multiple(Show(title=title) for title in args.title)

add_parser = commands.add_parser('add', help='Add show to collection.')
add_parser.add_argument('title', nargs='+')
add_parser.set_defaults(func=add_show)


class AddShowCommand(Command):
    name = 'add'
    help = 'Add show to collection'
    arguments = [('title', {'nargs': '+'})]

    def run(self):
        self.run()


def list_shows(args):
    print Show.all()

add_parser = commands.add_parser('list', help='List all shows in collection.')
add_parser.set_defaults(func=list_shows)


def main():
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
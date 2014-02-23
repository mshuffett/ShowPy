import sqlite3
from cement.core import backend, foundation, controller, handler

from database import Db, Show

class Shows(object):
    _TABLE_NAME = 'shows'
    def __init__(self):
        self._conn = sqlite3.connect('showpy.db')
        self.create_table_if_doesnt_exist()

    def create_table_if_doesnt_exist(self):
        with self._conn:
            self._conn.execute('CREATE TABLE if not exists %s (title)' % self._TABLE_NAME)

    def list(self):
        with self._conn:
            return self._conn.execute('SELECT * from shows').fetchall()

    def add_show(self, title):
        with self._conn:
            self._conn.execute('INSERT INTO shows VALUES (?)', (title,))

    def __str__(self):
        return 'Show 1, Show 2'


# define an application base controller
class BaseController(controller.CementBaseController):
    class Meta(object):
        label = 'base'
        description = 'ShowPy manages your shows.'

        config_defaults = {'shows': Shows()}

    def _setup(self, base_app):
        super(BaseController, self)._setup(base_app)
        self.shows = Shows()

    @controller.expose(hide=True)
    def default(self):
        app.args.print_help()

    @controller.expose(aliases=['ls'], help='Prints show list.')
    def list(self):
        print self.shows

class ShowPy(foundation.CementApp):
    class Meta(object):
        label = 'showpy'
        base_controller = BaseController


def main():
    db = Db.instance()
    app = ShowPy()
    try:
        app.setup()
        app.run()
    finally:
        # close the app
        app.close()


if __name__ == '__main__':
    main()
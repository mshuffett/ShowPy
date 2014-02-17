from cement.core import backend, foundation, controller, handler

class Shows(object):
    def list(self):
        return ['show1', 'show2']

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

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        app.args.print_help()

    @controller.expose(aliases=['ls'], help='Prints show list.')
    def list(self):
        print self.shows

class ShowPy(foundation.CementApp):
    class Meta(object):
        label = 'showpy'
        base_controller = BaseController

# create the app
app = ShowPy()

try:
    # setup the application
    app.setup()

    # run the application
    app.run()
finally:
    # close the app
    app.close()
"""
__init__.py for mlpyqtgraph, only functions and classes which are meant to be
used as interface
"""

from mlpyqtgraph import windows
from mlpyqtgraph import axes
from mlpyqtgraph import workers
from mlpyqtgraph import config_options as config


from . import ml_functions
from .ml_functions import *


GUIAgency = controllers.GUIAgency
GUIAgency.add_agent('figure', windows.FigureWindow)
GUIAgency.add_agent('axis', axes.Axis2D)


def plotter(func):
    """ Decorator for end user functions, adding figure functionality"""
    def func_wrapper(*args, **kwargs):
        """ Wrapper """
        gui_agency = GUIAgency(worker=func, *args, **kwargs)
        gui_agency.worker_agency.add_container('figure', workers.FigureWorker)
        gui_agency.worker_agency.add_container('axis', workers.AxisWorker)
        gui_agency.kickoff()
        return gui_agency.result
    return func_wrapper


# Check out
# https://stackoverflow.com/questions/653368/how-to-create-a-decorator-that-can-be-used-either-with-or-without-parameters
# for more on decorators with and without input arguments...

# The decorator stuff should really move the into the pqthreads package

def plottero(**options):
    """ Decorator for end user functions, adding figure functionality"""
    if len(options) > 0:
        config.options.set_options(**options)
    def wrap(func):
        """ Wrapper """
        def func_wrapper(*args, **kwargs):
            """ Wrapper """
            gui_agency = GUIAgency(worker=func, *args, **kwargs)
            gui_agency.worker_agency.add_container('figure', workers.FigureWorker)
            gui_agency.worker_agency.add_container('axis', workers.AxisWorker)
            gui_agency.kickoff()
            return gui_agency.result
        return func_wrapper
    return wrap

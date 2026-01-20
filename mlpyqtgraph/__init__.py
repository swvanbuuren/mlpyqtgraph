"""
__init__.py for mlpyqtgraph, only functions and classes which are meant to be
used as interface
"""

from pyqtgraph.Qt import QtCore
from pqthreads import config as pqthreads_config
from pqthreads.decorator import DecoratorCore, Decorator
from mlpyqtgraph import windows
from mlpyqtgraph import axes
from mlpyqtgraph import workers
from mlpyqtgraph import config

from . import ml_functions
from .ml_functions import *


__version__ = '0.9.1'


pqthreads_config.params.signal_slot_timeout = 10_000
pqthreads_config.params.set_application_attribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)


class OptionsDecoratorCore(DecoratorCore):
    """ Decorator take also takes keyword arguments and sets them as config
    options """

    def __init__(self, **options):
        super().__init__(**options)
        if options:
            config.options.set_options(**options)


OptionsDecoratorCore.add_agent('figure', windows.FigureWindow, workers.FigureWorker)
OptionsDecoratorCore.add_agent('axis',axes.Axis, workers.AxisWorker)
plotter = Decorator(OptionsDecoratorCore)

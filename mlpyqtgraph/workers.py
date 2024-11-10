"""
This modules defines all worker thread related classes and instances
"""

from pqthreads import containers
from pqthreads import refs


class AxisWorker(containers.WorkerItem):
    """ Worker thread axis to Control AxisWidget on the GUI thread """
    factory = containers.WorkerItem.get_factory()
    row = factory.attribute()
    column = factory.attribute()
    add = factory.method()
    surf = factory.method()
    line = factory.method()
    add_legend = factory.method()
    grid = factory.attribute()
    xlim = factory.attribute()
    ylim = factory.attribute()
    xlabel = factory.attribute()
    ylabel = factory.attribute()
    xticks = factory.attribute()
    yticks = factory.attribute()
    set_xticks = factory.method()
    set_yticks = factory.method()
    azimuth = factory.attribute()
    elevation = factory.attribute()


class FigureWorker(containers.WorkerItem):
    """ Worker thread figure to control FigureWindow on the GUI thread"""
    factory = containers.WorkerItem.get_factory()
    width = factory.attribute()
    height = factory.attribute()
    raise_window = factory.method()
    change_layout = factory.method()
    add_axis = factory.method()
    has_axis = factory.method()

    def __init__(self, *args, **kwargs):
        self.axis = None
        super().__init__(*args, **kwargs)

    def create_axis(self, *args, **kwargs):
        """ Adds an axis to the figure worker """
        if self.axis:
            return
        axis_container = refs.worker.get('axis')
        axis = axis_container.create(**kwargs)
        index = axis.index
        self.add_axis(index)
        self.axis = axis

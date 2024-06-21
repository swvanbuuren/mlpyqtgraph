"""
This modules defines all worker thread related classes and instances
"""

from pqthreads import controllers
from pqthreads import containers


class AxisWorker(containers.WorkerItem):
    """ Worker thread axis to Control AxisWidget on the GUI thread """
    factory = containers.WorkerItem.get_factory()
    row = factory.attribute()
    column = factory.attribute()
    add = factory.method()
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


class FigureWorker(containers.WorkerItem):
    """ Worker thread figure to control FigureWindow on the GUI thread"""
    factory = containers.WorkerItem.get_factory()
    width = factory.attribute()
    height = factory.attribute()
    raise_window = factory.method()
    create_axis = factory.method()
    change_layout = factory.method()
    change_axis = factory.method()

    def __init__(self, *args, **kwargs):
        self.axes = []
        super().__init__(*args, **kwargs)
        self.add_axis()

    def add_axis(self, *args, **kwargs):
        """ Adds an axis to the figure worker """
        axis_container = controllers.worker_refs.get('axis')
        axis = axis_container.create(**kwargs)
        self.create_axis(axis.index, **kwargs)
        self.axes.append(axis.index)

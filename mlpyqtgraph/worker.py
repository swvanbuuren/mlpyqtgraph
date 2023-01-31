"""
This modules defines all worker thread related classes and instances

"""
import weakref
import mlpyqtgraph.controllers as controllers
import mlpyqtgraph.descriptors as descr


class AxisWorker:
    """ Worker thread axis to Control AxisWidget on the GUI thread """
    descriptor_factory = descr.DescriptorFactory(controllers.worker_controller.axis_sender)
    row = descriptor_factory.attribute()
    column = descriptor_factory.attribute()
    add = descriptor_factory.method()
    add_legend = descriptor_factory.method()
    grid = descriptor_factory.attribute()
    xlim = descriptor_factory.attribute()
    ylim = descriptor_factory.attribute()
    xlabel = descriptor_factory.attribute()
    ylabel = descriptor_factory.attribute()
    xticks = descriptor_factory.attribute()
    yticks = descriptor_factory.attribute()
    set_xticks = descriptor_factory.method()
    set_yticks = descriptor_factory.method()

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return f'AxisWorker(index={self.index})'


class AxesContainer:
    """ Container for Axis """
    def __init__(self):
        self.axes = list()
        self.current = None

    def __repr__(self):
        repr_string = '['
        for idx, axis in enumerate(self.axes):
            if idx > 0:
                repr_string += ', '
            repr_string += repr(axis)
        repr_string += ']'
        return repr_string

    def create(self, index, *args, **kwargs):
        """ Create a new FigureWorker and return a weak reference proxy """
        self.append(AxisWorker(index, *args, **kwargs))
        self.current = self.back()
        return weakref.proxy(self.back())

    def append(self, item):
        """ Append an item """
        self.axes.append(item)

    def back(self):
        """ Returns the last item """
        return self.axes[-1]


axes_container = AxesContainer()


class FigureWorker:
    """ Worker thread figure to control FigureWindow on the GUI thread"""
    controller = controllers.worker_controller.figure_sender
    descriptor_factory = descr.DescriptorFactory(controller)
    width = descriptor_factory.attribute()
    height = descriptor_factory.attribute()
    raise_window = descriptor_factory.method()
    create_axis = descriptor_factory.method()
    change_layout = descriptor_factory.method()
    change_axis = descriptor_factory.method()

    def __init__(self, *args, **kwargs):
        self.axes = list()
        self.index = self.controller.create(*args, **kwargs)
        self.add_axis()

    def __repr__(self):
        return f'FigureWorker(index={self.index})'

    def activate(self):
        """ Sets this figure a current figure and raises it to top """
        self.raise_window()

    def close(self):
        """ Closes the current figure on the GUI side """
        self.controller.delete(self.index)

    def add_axis(self, *args, **kwargs):
        """ Adds an axis to the figure worker """
        axis_index = self.create_axis(*args, **kwargs)
        axis = axes_container.create(axis_index)
        self.axes.append(axis)


class FiguresContainer:
    """ Container for FigureWorkers """
    def __init__(self):
        self.figures = list()
        self.current = None

    def __repr__(self):
        repr_string = '['
        for idx, figure in enumerate(self.figures):
            if idx > 0:
                repr_string += ', '
            repr_string += repr(figure)
        repr_string += ']'
        return repr_string

    def create(self, *args, **kwargs):
        """ Create a new FigureWorker and return a weak reference proxy """
        self.append(FigureWorker(*args, **kwargs))
        self.current = self.back()
        return weakref.proxy(self.back())

    def append(self, item):
        """ Append an item """
        self.figures.append(item)

    def back(self):
        """ Returns the last item """
        return self.figures[-1]

    def close(self, item):
        """
        Remove an item from the container, closes its figure and deletes it.
        After calling this function, weak references to this item will no longer
        be valid.
        """
        index = self.figures.index(item)
        figure_worker = self.figures.pop(index)
        figure_worker.close()
        del figure_worker


figures_container = FiguresContainer()


class PlotWidgetWorker:
    """ PlotWidget item for the worker thread """
    def __init__(self):
        pass

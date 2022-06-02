""" Matlab like functions for easy matlab like figure and plot definitions """
import mlpyqtgraph.worker as worker


def figure(*args, **kwargs):
    """ Create, raise or modify FigureWorker objects """
    if not args:
        return worker.figures_container.create(**kwargs)
    figure_worker = args[0]
    figure_worker.activate()
    worker.figures_container.current = figure_worker
    return figure_worker

def gcf():
    """ Returns the current figure """
    return worker.figures_container.current


def gca():
    """ Returns the current axis """
    return worker.axes_container.current


def close(figure_ref):
    """ Closes the provided figure and deletes it """
    gcf().close(figure_ref)


def plot(*args, **kwargs):
    """ Plots into the current axis """
    return gca().add(*args, **kwargs)


def subplot(*args, **kwargs):
    """ Create subplot and return its axis"""
    return gcf().add_axis(*args, **kwargs)


def legend(*args):
    """ Adds a legend to the current figure """
    gca().add_legend(*args)


def surf(*args, **kwargs):
    """ Plots a 3D surface """
    if gcf().change_layout('Qt'):
        gcf().change_axis('3D')
        gcf().add_axis()
    gca().add(*args, **kwargs)

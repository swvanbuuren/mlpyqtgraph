"""
Matplotlib-like functions for easy figure and plot definitions
"""

from pqthreads import controllers


def figure(*args, **kwargs):
    """ Create, raise or modify FigureWorker objects """
    container = controllers.worker_refs.get('figure')
    if not args:
        return container.create(**kwargs)
    figure_worker = args[0]
    figure_worker.activate()
    container.current = figure_worker
    return figure_worker

def gcf():
    """ Returns the current figure """
    container = controllers.worker_refs.get('figure')
    return container.current


def gca():
    """ Returns the current axis """
    container = controllers.worker_refs.get('axis')
    if container.current is None:
        figure()  # make sure we always have a figure
    return container.current


def close(figure_ref):
    """ Closes the provided figure and deletes it """
    gcf().close(figure_ref)


def plot(*args, **kwargs):
    """ Plots into the current axis """
    gcf().create_axis(axis_type='2D')
    return gca().add(*args, **kwargs)


def legend(*args):
    """ Adds a legend to the current figure """
    gca().add_legend(*args)


def surf(*args, **kwargs):
    """ Plots a 3D surface """
    gcf().change_layout('Qt')
    gcf().create_axis(axis_type='3D')
    gca().add(*args, **kwargs)

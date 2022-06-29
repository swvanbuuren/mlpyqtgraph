"""
Module for controlling of and communication between worker and GUI thread
"""
import sys
import pyqtgraph.Qt.QtWidgets as QtWidgets
import pyqtgraph.Qt.QtCore as QtCore

import mlpyqtgraph.windows as windows
import mlpyqtgraph.axes as axes
import mlpyqtgraph.thread_communicator as tc


class RootException(Exception):
    """ Root Exception of the threads module """


class SlotException(RootException):
    """ This Exception is raised if no signal was sent to a slot """


class WorkerException(RootException):
    """ This Exception is raised if an error was raised in the worker thread """


class GUIItemException(RootException):
    """ This Exception is raised if an error was raised in the worker thread """


class WorkerController(QtCore.QObject):
    """ Controller class, to be used in the worker thread """
    error = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure_sender = tc.Sender('figure')
        self.axis_sender = tc.Sender('axis')


worker_controller = WorkerController()


class GUIItemContainer(QtCore.QObject):
    """
    Controller for a container with instances of user-supplied GUI element class
    """

    def __init__(self, item_class, parent=None):
        super().__init__(parent)
        self.items = list()
        self.item_class = item_class

    def __repr__(self):
        return f'GUIItemContainer(item_class={self.item_class.__name__})'

    @property
    def count(self):
        """ Current number of items """
        return len(self.items)

    def back(self):
        """ Returns the last item """
        return self.items[-1]

    def create(self, args, kwargs):
        """ Creates a new item instance with user-supplied item class """
        index = self.count
        new_item = self.item_class(index, *args, **kwargs)
        self.items.append(new_item)
        return index

    def request(self, index, args):
        """ Returns values of item attributes """
        item = self.items[index]
        return [getattr(item, arg) for arg in args]

    def modify(self, index, kwargs):
        """ Modifies item's attributes"""
        item = self.items[index]
        for key, value in kwargs.items():
            setattr(item, key, value)

    def method(self, index, func_name, args, kwargs):
        """ Execute method on item """
        try:
            item = self.items[index]
        except IndexError as err:
            raise GUIItemException(f'Index not find for {self.item_class} items') from err
        func = getattr(item, func_name)
        return func(*args, **kwargs)

    def delete(self, index):
        """ Deletes the item at index """
        item = self.items.pop(index)
        item.delete()
        del item


class GUIItemFactory:
    """ Factory for GUI Item instances coordinate by a GUIItemContainer """
    def __init__(self, container):
        self.container = container

    def produce(self, *args, **kwargs):
        """ Produce a new item """
        index = self.container.create(args, kwargs)
        item = self.container.back()
        return index, item


class FunctionRunnable(QtCore.QRunnable):
    """
    QRunnable subclass that runs a user-supplied functions with exception
    handling
    """
    def __init__(self, worker_function, parent=None):
        super().__init__(parent)
        self.controller = worker_controller
        self.worker_function = worker_function

    def run(self):
        try:
            self.worker_function()
        except tc.ReceiverException:
            pass # already handled ad receiver side
        except BaseException:
            (exception_type, value, traceback) = sys.exc_info()
            sys.excepthook(exception_type, value, traceback)
            self.controller.error.emit()


class GUIController(QtCore.QObject):
    """ Controller class which coordinates all figure and axis objects """
    def __init__(self, worker, parent=None):
        super().__init__(parent)
        self.exception_raised = False
        self.application = QtWidgets.QApplication(sys.argv)
        self.threadpool = QtCore.QThreadPool()
        self.setup_controllers()
        self.execute(worker)

    def setup_controllers(self):
        """ Setup all controllers """
        self.axis_container = GUIItemContainer(axes.factory)
        FigureWindow = windows.FigureWindow
        FigureWindow.axis_factory = GUIItemFactory(self.axis_container)
        self.figure_container = GUIItemContainer(FigureWindow)
        self.axis_receiver = tc.Receiver(self.axis_container)
        self.figure_receiver = tc.Receiver(self.figure_container)

    def execute(self, worker):
        """ Create QApplication, start worker thread and the main event loop """
        self.start(worker)
        try:
            self.application.exec_()
        except tc.SenderException:
            if not self.exception_raised:
                raise
            self.exception_raised = False
        finally:
            self.application.exit()

    def start(self, worker):
        """ Starts the worker thread with driver function """
        runnable = FunctionRunnable(worker)
        runnable.controller.error.connect(self.worker_exception)
        runnable.controller.figure_sender.connect_receiver(self.figure_receiver)
        runnable.controller.axis_sender.connect_receiver(self.axis_receiver)
        self.threadpool.start(runnable)

    @QtCore.Slot()
    def worker_exception(self):
        """ Slot to react on a work exception """
        self.exception_raised = True

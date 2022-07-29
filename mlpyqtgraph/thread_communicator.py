"""
Thread communicator
===================

Thread communicator module for sending and receiving information from one thread to another using a
sender and receiver
"""


from copy import copy
from contextlib import contextmanager
import pyqtgraph.Qt.QtCore as QtCore


class RootTCException(Exception):
    """ Root Exception of the threads module """


class SenderException(RootTCException):
    """ This Exception is raised if no signal was sent to a slot and thus no message was received"""


class ReceiverException(RootTCException):
    """ This Exception is raised if an error at receiver side was detected """


@contextmanager
def wait_signal(signal, timeout=1000):
    """Block loop until signal emitted, or timeout (ms) elapses."""
    loop = QtCore.QEventLoop()
    signal.connect(loop.quit)
    yield
    if timeout is not None:
        QtCore.QTimer.singleShot(timeout, loop.quit)
    loop.exec_()


class Sender(QtCore.QObject):
    """ Enables exchange of data with Receiver using signal/slots """
    createSignal = QtCore.Signal(list, dict)
    modifySignal = QtCore.Signal(int, dict)
    requestSignal = QtCore.Signal(int, list)
    methodSignal = QtCore.Signal(int, str, list, dict)
    deleteSignal = QtCore.Signal(int)

    dataRecevied = QtCore.Signal()

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.no_message = object()
        self.receiver_error = False
        self.message = self.no_message
        self.name = name

    def __repr__(self):
        return f'Sender(name={self.name})'

    def connect_receiver(self, receiver):
        """ Connects the sender to a receiver """
        receiver.signal.connect(self.slot)
        receiver.error.connect(self.error_detected)
        self.createSignal.connect(receiver.create_slot)
        self.modifySignal.connect(receiver.modify_slot)
        self.requestSignal.connect(receiver.request_slot)
        self.methodSignal.connect(receiver.method_slot)
        self.deleteSignal.connect(receiver.delete_slot)

    def create(self, *args, **kwargs):
        """ Send out a signal and obtain data from receiver"""
        with wait_signal(self.dataRecevied):
            self.createSignal.emit(args, kwargs)
        return self.read_message()

    def modify(self, index, **kwargs):
        """ Send out a one-way signal with given arguments and keyword arguments """
        self.modifySignal.emit(index, kwargs)

    def request(self, index, *args):
        """ Obtain data from receiver"""
        with wait_signal(self.dataRecevied):
            self.requestSignal.emit(index, args)
        return self.read_message()

    def method(self, index, func_name, *args, **kwargs):
        """ Send out a signal to execute a method on the receiver class """
        with wait_signal(self.dataRecevied):
            self.methodSignal.emit(index, func_name, args, kwargs)
        return self.read_message()

    def delete(self, index):
        """ Send out a signal to delete object at index on the receiver class """
        self.closeSignal.emit(index)

    def read_message(self):
        """ Helper method, that reads message set by slot and returns a copy """
        if self.message is self.no_message:
            if self.receiver_error:
                raise ReceiverException('Error detected at receiver side')
            raise SenderException('No message received')
        message = copy(self.message)
        self.message = self.no_message
        return message

    @QtCore.Slot(dict)
    def slot(self, data):
        """ Slot for receiving data """
        self.message = data
        self.dataRecevied.emit()

    def error_detected(self):
        """ If a receiver error is detected ... """
        self.receiver_error = True


class Receiver(QtCore.QObject):
    """ A receiver for operations whose instructions were sent by Sender """
    signal = QtCore.Signal(dict)
    error = QtCore.Signal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.create = controller.create
        self.modify =  controller.modify
        self.request = controller.request
        self.method = controller.method
        self.delete = controller.delete

    def __repr__(self):
        return f'Receiver(controller={self.controller})'

    @contextmanager
    def register_exception(self):
        """ Register errors at receiver side """
        try:
            yield
        except BaseException:
            self.error.emit()
            raise

    @QtCore.Slot(list, dict)
    def create_slot(self, args, kwargs):
        """ Slot for creating a new class instance """
        with self.register_exception():
            self.signal.emit(self.create(args, kwargs))

    @QtCore.Slot(int, dict)
    def modify_slot(self, index, kwargs):
        """ Slot for modifying an instance attribute """
        self.modify(index, kwargs)

    @QtCore.Slot(int, list)
    def request_slot(self, index, args):
        """ Slot for requesting an instance attribute """
        with self.register_exception():
            self.signal.emit(self.request(index, args))

    @QtCore.Slot(int, str, list, dict)
    def method_slot(self, index, func, args, kwargs):
        """ Slot for calling a class instance method """
        with self.register_exception():
            self.signal.emit(self.method(index, func, args, kwargs))

    @QtCore.Slot(int)
    def delete_slot(self, index):
        """ Slot for closing/deleting a class instance object at index """
        self.delete(index)

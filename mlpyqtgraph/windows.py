"""
This module contains all classes for handling the GUI figures and axes in mlpyqtgraph

"""

import sys
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
from pqthreads import controllers


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class RootException(Exception):
    """ Root Exception of the windows module """


class NoFigureException(RootException):
    """ This Exception is raised if no figure is defined, although one is requested """


class NoFigureLayout(RootException):
    """ This Exception is raised the figure layout has not been set """


class GridLayoutWidget(QtWidgets.QWidget):
    """ Custom layout widget with GridLayout to mimic pyqtgraph's layout widget """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def getItem(self, row, column):
        """ Returns the item at row, col. If empty return None """
        return self.layout().itemAtPosition(row, column)

    def addItem(self, item, row, column, rowSpan=1, columnSpan=1):
        """ Adds an item at row, col with rowSpand and colSpan """
        self.layout().addWidget(item, row, column, rowSpan, columnSpan)


class FigureWindow(QtCore.QObject):
    """ Controls a figure window instance """
    triggered = QtCore.Signal()
    axis_factory = None

    def __init__(self, index, title='Figure', width=600, height=500, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.layout_type = 'None'
        self.axis_type = '2D'
        self.window = self.setup_window(parent, width, height)
        self.change_layout()
        self.title = f'Figure {index+1}: {title}'
        self.window.show()

    def setup_window(self, parent, width, height):
        """ Setup the figure window as QMainWindow """
        window = QtWidgets.QMainWindow(parent)
        window.resize(width, height)
        return window

    def change_axis(self, axis_type='2D'):
        """
        Change the figure's axis type; 2D for Axis2D or 3D for Axis3D

        Returns: boolean indicating layout change
        """
        self.axis_type = axis_type

    def change_layout(self, layout_type='pg'):
        """
        Change the figure's layout type; pg for pyqtgraph's native layout or Qt layout

        Returns: boolean indicating layout change
        """
        LayoutWidget = pg.GraphicsLayoutWidget
        if self.layout_type == layout_type:
            return False
        self.layout_type = layout_type
        if self.layout_type == 'Qt':
            LayoutWidget = GridLayoutWidget
        self.window.setCentralWidget(LayoutWidget())
        return True

    def create_axis(self, index, row=0, column=0, row_span=1, column_span=1):
        """ Creates an axis and return its index """
        if self.graphics_layout.getItem(row, column):
            return
        axis = controllers.gui_refs.get('axis').items[index]
        self.graphics_layout.addItem(axis, row, column, row_span, column_span)

    @property
    def graphics_layout(self):
        """ Returns the GraphicsLayoutWidget """
        return self.window.centralWidget()

    @property
    def title(self):
        """ Figure window title """
        return self.window.windowTitle()

    @title.setter
    def title(self, new_title):
        self.window.setWindowTitle(new_title)

    @property
    def width(self):
        """ Figure window width """
        return self.window.width()

    @width.setter
    def width(self, width):
        self.window.resize(width, self.height)

    @property
    def height(self):
        """ Figure window height """
        return self.window.height()

    @height.setter
    def height(self, height):
        self.window.resize(self.width, height)

    def raise_window(self):
        """ Raises the current window to top """
        if sys.platform == 'win32':
            state = self.window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive
            self.window.setWindowState(state)
            self.window.activateWindow()
        else:
            self.window.raise_()

    def delete(self):
        """ Closes the window """
        self.window.close()


class Figure3DWindow(FigureWindow):
    """ Controls a 3D figure window instance """


class Figure2DWindow(FigureWindow):
    """ Controls a 2D figure window instance """

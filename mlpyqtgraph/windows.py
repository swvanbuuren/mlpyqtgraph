"""
This module contains all classes for handling the GUI figures and axes in mlpyqtgraph

"""

import sys
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
from pqthreads import refs


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class RootException(Exception):
    """ Root Exception of the windows module """


class NoFigureException(RootException):
    """ This Exception is raised if no figure is defined, although one is requested """


class NoFigureLayout(RootException):
    """ This Exception is raised the figure layout has not been set """


class FigureWindow(QtCore.QObject):
    """ Controls a figure window instance """
    triggered = QtCore.Signal()
    axis_factory = None

    def __init__(self, index, title='Figure', width=600, height=500, layout_type='pg', parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.layout_type = None
        self.window = self.setup_window(parent, width, height)
        self.change_layout(layout_type)
        self.title = f'Figure {index+1}: {title}'
        self.window.show()

    def setup_window(self, parent, width, height):
        """ Setup the figure window as QMainWindow """
        window = QtWidgets.QMainWindow(parent)
        window.resize(width, height)
        return window

    def change_layout(self, layout_type='pg'):
        """
        Change the figure's layout type; 'pg' for pyqtgraph's native layout or 'Qt'
        layout.

        Returns: boolean indicating layout change
        """
        if self.layout_type == layout_type:
            return False
        self.layout_type = layout_type
        LayoutWidget = pg.GraphicsLayoutWidget
        if layout_type == 'Qt':
            LayoutWidget = pg.opengl.GLViewWidget
        self.window.setCentralWidget(LayoutWidget())
        return True

    def add_axis(self, index):
        """ Adds an axis to the figure """
        axis = refs.gui.get('axis').items[index]
        self.graphics_layout.addItem(axis)

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

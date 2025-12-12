"""Demonstrate removal and addition of child items in a GLGraphicsItem."""

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import mkQApp, QtCore
from mlpyqtgraph.axes import Axis3D
from mlpyqtgraph.grid_axes import GLGridAxis


def main():
    """Run the GLGraphicsItem remove/add example."""
    mkQApp("Removal Example")

    w = gl.GLViewWidget()
    w.setWindowTitle('GL')
    w.setGeometry(0, 110, 800, 600)
    w.show()

    # Create our custom item
    grid_axes = GLGridAxis()
    w.addItem(grid_axes)

    lim=10.0
    new_coords = {
        'x': [-lim, 0.0, lim],
        'y': [-lim, 0.0, lim],
        'z': [-lim, 0.0, lim],
    }
    new_limits = {
        'x': (-1.05*lim, 1.05*lim),
        'y': (-1.05*lim, 1.05*lim),
        'z': (-1.05*lim, 1.05*lim),
    }

    def change():
        grid_axes.setData(coords=new_coords, limits=new_limits)
        w.setCameraPosition(**grid_axes.best_camera())

    QtCore.QTimer.singleShot(1000, change)

    pg.exec()


if __name__ == '__main__':
    main()

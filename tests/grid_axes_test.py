"""Demonstrate removal and addition of child items in a GLGraphicsItem."""

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import mkQApp, QtCore
from mlpyqtgraph.grid_axes import GLGridAxis
from mlpyqtgraph.config import options


def main():
    """Run the GLGraphicsItem remove/add example."""
    options.set_options(black_on_white=False)

    mkQApp("Removal Example")

    w = gl.GLViewWidget()
    w.show()

    # Create our custom item
    grid_axes = GLGridAxis()
    w.addItem(grid_axes)

    lim=10.0
    new_coords = {
        'x': [-lim, 0.0, lim],
        'y': [-lim, 0.0, 0.75*lim],
        'z': [-1.5*lim, 0.0, lim],
    }
    new_limits = {
        'x': (1.05*new_coords['x'][0], 1.05*new_coords['x'][-1]),
        'y': (1.05*new_coords['y'][0], 1.05*new_coords['y'][-1]),
        'z': (1.05*new_coords['z'][0], 1.05*new_coords['z'][-1]),
    }

    def change():
        grid_axes.setData(coords=new_coords, limits=new_limits)
        w.setCameraPosition(**grid_axes.best_camera())

    QtCore.QTimer.singleShot(1000, change)

    pg.exec()


if __name__ == '__main__':
    main()

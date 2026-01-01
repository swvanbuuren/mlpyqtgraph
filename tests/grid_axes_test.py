"""Demonstrate removal and addition of child items in a GLGraphicsItem."""

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import mkQApp, QtCore
from mlpyqtgraph.grid_axes import GLGridAxis
from mlpyqtgraph.config import options


def float_to_str(*args, decimals=1):
    return [f'{x:.{decimals}f}' for x in args]


def main():
    """Run the GLGraphicsItem remove/add example."""
    options.set_options(black_on_white=True)

    mkQApp("GLGridAxis Modification Example")

    w = gl.GLViewWidget()
    w.show()

    grid_axes = GLGridAxis()
    w.addItem(grid_axes)
    w.setCameraPosition(**grid_axes.best_camera())

    lim=10.0
    new_coords = {
        'x': [-lim, 0.0, lim],
        'y': [-lim, 0.0, lim],
        'z': [-3/4*lim, -3/8*lim, 0.0, 3/8*lim, 3/4*lim],
    }
    new_coords_labels = {
        'x': float_to_str(-lim, 0.0, lim),
        'y': float_to_str(-lim, 0.0, 0.75*lim),
        'z': float_to_str(-2, -1, 0.0, 1, 2),
    }
    new_limits = {
        'x': (1.05*new_coords['x'][0], 1.05*new_coords['x'][-1]),
        'y': (1.05*new_coords['y'][0], 1.05*new_coords['y'][-1]),
        'z': (1.05*new_coords['z'][0], 1.05*new_coords['z'][-1]),
    }

    def change():
        grid_axes.setData(coords=new_coords, coords_labels=new_coords_labels, limits=new_limits)
        w.setCameraPosition(**grid_axes.best_camera())

    QtCore.QTimer.singleShot(1000, change)

    pg.exec()


if __name__ == '__main__':
    main()

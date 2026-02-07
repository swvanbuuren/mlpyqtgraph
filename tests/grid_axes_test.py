"""Demonstrate removal and addition of child items in a GLGraphicsItem."""

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph import mkQApp, QtCore, QtWidgets
from mlpyqtgraph.grid_axes import GLGridAxisItem
from mlpyqtgraph.config import options


def float_to_str(*args, decimals=1):
    return [f'{x:.{decimals}f}' for x in args]

def gen_surface_plt():
    extent = 10
    points = 36
    amplitude = 10
    frequency = 1
    x = np.linspace(-extent, extent, points)
    y = np.linspace(-extent, extent, points)
    z = np.zeros((points, points))
    for i in range(points):
        yi = y[i]
        d = np.hypot(x, yi)
        z[:,i] = amplitude * np.cos(frequency*d) / (d+1)

    surface = gl.GLSurfacePlotItem(
        x=x, y=y, z=z,
        shader='heightColor',
        showGrid=True,
        lineColor=(0.25,0.25,0.25,1)
    )
    surface.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
    return surface


def main():
    """Run the GLGraphicsItem remove/add example."""
    options.set_options(black_on_white=True)

    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    mkQApp("GLGridAxisItem Modification Example")

    w = gl.GLViewWidget()
    w.show()

    grid_axes = GLGridAxisItem(line_antialias=True)
    w.addItem(grid_axes)
    s1 = gen_surface_plt()
    w.addItem(s1)
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

    w2 = gl.GLViewWidget()
    w2.show()

    s2 = gen_surface_plt()
    w2.addItem(s2)

    grid_axes2 = GLGridAxisItem(coords=new_coords, coords_labels=new_coords_labels, limits=new_limits, line_antialias=True)
    w2.addItem(grid_axes2)
    w2.setCameraPosition(**grid_axes2.best_camera())

    pg.exec()


if __name__ == '__main__':
    main()

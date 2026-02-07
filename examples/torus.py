"""
Basic example that shows surface plots of mlpyqtgraph
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Examples with surface plots """
    nx, ny = 25, 25
    R = 3.0  # major radius
    r = 1.0  # minor radius
    u = np.linspace(0, 2*np.pi, nx)
    v = np.linspace(0, 2*np.pi, ny)
    u_grid, v_grid = np.meshgrid(u, v, indexing='ij')
    x = (R + r * np.cos(v_grid)) * np.cos(u_grid)
    y = (R + r * np.cos(v_grid)) * np.sin(u_grid)
    z = r * np.sin(v_grid)

    mpg.figure(title='Perspective surface plot')
    mpg.surf(x, y, z)
    ax = mpg.gca()
    ax.zlim = (-4, 4)


if __name__ == '__main__':
    main()

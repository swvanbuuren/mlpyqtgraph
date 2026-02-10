"""
Basic example that shows a saddle surface plot and the corresponding points.
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Examples with surface plots """
    nx, ny = 20, 20
    x = np.linspace(-8, 8, nx)
    y = np.linspace(-8, 8, ny)
    z = 0.1 * ((x.reshape(ny,1) ** 2) - (y.reshape(1,nx) ** 2))

    xp = np.repeat(x, y.size)
    yp = np.tile(y, x.size)
    zp = z.flatten()

    mpg.figure(title='Saddle example')
    mpg.surf(x, y, z)
    mpg.points3(xp, yp, zp, color=(0.8, 0.1, 0.1, 1), size=3)


if __name__ == '__main__':
    main()

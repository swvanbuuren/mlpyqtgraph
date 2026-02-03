"""
Basic example that shows surface plots of mlpyqtgraph
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Examples with surface plots """
    extent = 10
    nx = 36
    ny = 36
    amplitude = 10
    frequency = 1
    x = np.linspace(-extent, extent, nx)
    y = np.linspace(-extent, extent, ny)
    z = np.zeros((nx, ny))
    for i in range(ny):
        yi = y[i]
        d = np.hypot(x, yi)
        z[:,i] = amplitude * np.cos(frequency*d) / (d+1)

    mpg.figure(title='Perspective surface plot')
    mpg.surf(x, y, z)


if __name__ == '__main__':
    main()

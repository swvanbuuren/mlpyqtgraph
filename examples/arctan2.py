"""
Surface plot of arctan2 function
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Examples with surface plots """
    extent = 4
    nx = 48
    ny = 48
    amplitude = 1.0
    x = np.linspace(-extent, extent, nx)
    y = np.linspace(-extent, extent, ny)
    z = np.zeros((nx, ny))
    for i in range(ny):
        z[i, :] = amplitude * np.arctan2(x, y[i])

    mpg.figure(title='arctan2(x, y)', layout_type='Qt')
    mpg.surf(x, y, z)
    ax = mpg.gca()
    ax.aspect_ratio = 'flat'
    ax.azimuth = 315
    ax.projection = 'orthographic'

if __name__ == '__main__':
    main()

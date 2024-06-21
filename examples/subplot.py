"""
Basic example that shows subplot usage of mlpyqtgraph
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Example with subplots """
    fig = mpg.figure(title='Third figure')
    fig.width = 540
    fig.height = 440
    mpg.subplot(0,0)
    theta = np.linspace(0, 2*np.pi, 100)
    mpg.plot(theta, np.sin(theta))
    mpg.gca().grid = True
    mpg.subplot(0,1)
    mpg.plot(theta, np.cos(theta))
    mpg.subplot(1,0)
    mpg.plot(theta, np.tan(theta))
    mpg.subplot(1,1)
    mpg.plot(theta, np.arctan(theta))


if __name__ == '__main__':
    main()

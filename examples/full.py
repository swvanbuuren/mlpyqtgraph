"""
Advanced example with custom figure size, mmultiple lines and line color/style
adjustments
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Advanced mlpyqtgraph example """
    plot_args = {'width': 2}

    fig = mpg.figure(title='Another figure')
    fig.width = 600
    theta = np.linspace(0, 2*np.pi, 100)
    mpg.plot(theta, np.cos(theta), **plot_args)
    mpg.plot(theta, np.sin(theta), **plot_args)
    mpg.plot(theta, np.sin(theta + np.pi), style='--', **plot_args)
    mpg.plot(theta, np.cos(theta + np.pi), style='.-', **plot_args)
    mpg.plot(theta, 0.5*np.cos(theta), color='k', **plot_args)
    mpg.gca().grid = True

if __name__ == '__main__':
    main()

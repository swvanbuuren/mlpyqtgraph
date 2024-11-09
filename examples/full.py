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
    axis = mpg.gca()
    axis.grid = True
    axis.xlabel = 'x'
    axis.ylabel = 'y'
    axis.xticks = (
        (0.0, '0'),
        (np.pi/2.0, 'π/2'),
        (np.pi, 'π'),
        (1.5*np.pi, '3π/2'),
        (2.0*np.pi, '2π'),
    )
    axis.add_legend(
        'y=cos(x)',
        'y=sin(x)',
        'y=sin(x+π)',
        'y=cos(x+π)',
        'y=cos(x)/2',
    )


if __name__ == '__main__':
    main()

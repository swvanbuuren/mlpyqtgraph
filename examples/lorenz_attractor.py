""" Plot3 example with Lorenz attractor """

import numpy as np
import mlpyqtgraph as mpg


def lorenz(x, *, s=10, r=28, b=2.667):
    """
    Parameters
    ----------
    x : array-like, shape (3,)
       Point of interest in three-dimensional space.
    s, r, b : float
       Parameters defining the Lorenz attractor.

    Returns
    -------
    x_dot : array, shape (3,)
       Values of the Lorenz attractor's partial derivatives at x.
    """
    return np.array([
        s*(x[1] - x[0]),
        r*x[0] - x[1] - x[0]*x[2],
        x[0]*x[1] - b*x[2]
    ])


def euler(dxdt, x0, dt=0.005, num_steps=10_000):
    """
    Euler integration

    Parameters
    ----------
    dxdt : callable
        Function that takes a single argument `x` with shape `(n,)` and
        returns an array with the same shape, representing the derivative
        of `x` with respect to time.
    x0 : array-like, shape `(n,)`
        Initial condition.
    dt : float, optional
        Time step. Defaults to 0.005.
    num_steps : int, optional
        Number of steps to run the integration. Defaults to 10_000.

    Returns
    -------
    x : array, shape `(n, num_steps + 1)`
        Path taken by the system during the integration.
    """
    x = np.empty((num_steps + 1, len(x0)))
    x[0] = x0
    for i in range(num_steps):
        x[i + 1] = x[i] + dt*dxdt(x[i])
    return x.T


@mpg.plotter
def main():
    """ Plot Lorenz attractor """
    x, y, z = euler(dxdt=lorenz, x0=(0., 1., 1.05))

    mpg.figure(title='Lorenz attractor', layout_type='Qt')
    mpg.plot3(x, y, z, projection='orthographic')
    ax = mpg.gca()
    ax.azimuth = 315


if __name__ == '__main__':
    main()

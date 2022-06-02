"""
First basic example of mlpyqtgraph
"""
import numpy as np
import mlpyqtgraph as mpg

# NOTE
# TO DO
# - Change Method and AttributeDescriptors -->
#   * Add property to class using decorator(with arguments) or metaclass

def plot_example():
    """ Examples for 2D plots """
    plot_args = {'width': 2}

    fig1 = mpg.figure(title='Test figure')
    fig1.width = 500
    fig1.height = 400
    mpg.plot(list(range(5)), [1, 3, 2, 0, 5], **plot_args)

    fig2 = mpg.figure(title='Another figure')
    fig2.width = 600
    theta = np.linspace(0, 2*np.pi, 100)
    mpg.plot(theta, np.cos(theta), **plot_args)

    fig3 = mpg.figure(title='Third figure')
    fig3.width = 540
    fig3.height = 440
    mpg.subplot(0,0)
    mpg.plot(theta, np.sin(theta), **plot_args)
    mpg.gca().grid = True
    mpg.subplot(0,1)
    mpg.plot(theta, np.cos(theta), **plot_args)
    mpg.subplot(1,0)
    mpg.plot(theta, np.tan(theta), **plot_args)
    mpg.subplot(1,1)
    mpg.plot(theta, np.arctan(theta), **plot_args)


def surf_example():
    """ Examples for surface plots """
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

    mpg.fig4 = mpg.figure(title='Fourth figure')
    mpg.surf(x, y, z, colormap='viridis', projection='perspective')

    mpg.fig5 = mpg.figure(title='Fourth figure')
    mpg.surf(x, y, z, colormap='viridis', projection='orthographic')


def main():
    """ Here we perform some calculations and try to plot some stuff .... """
    plot_example()
    surf_example()
    

if __name__ == '__main__':
    mpg.GUIController(worker=main)

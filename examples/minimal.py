"""
Basic example that shows minimal usage of mlpyqtgraph
"""

import mlpyqtgraph as mpg


@mpg.plotter
def main():
    """ Minimal mlpyqtgraph example """
    mpg.plot(range(5), (1, 3, 2, 0, 5))


if __name__ == '__main__':
    main()
